import json
import multiprocessing
import threading
import matplotlib.pyplot as plt
import tkinter as tk
import time
import ttkbootstrap as tkb


def annotate_graph(annotation_event, annotation_queue):
    while True:
        # if cleared: get the result value
        if not annotation_event.is_set():
            dialog_dict = annotation_queue.get()  # get data from the queue
            initial_value, edit = dialog_dict['value'], dialog_dict['edit']
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            if edit:
                dialog = EditAnnotation(root, "Input", initial_value=initial_value)
            else:
                dialog = CreateAnnotation(root, "Input", initial_value=initial_value)
            note_text = dialog.result
            dialog_dict = {"value": note_text, "edit": edit}
            annotation_queue.put(dialog_dict)  # put data back into the queue
            # re-set the event
            root.destroy()
            annotation_event.set()
        time.sleep(.1)


def annotator(figures):
    list_of_annotators = []
    annotation_event = multiprocessing.Event()
    annotation_queue = multiprocessing.Queue()
    threading.Thread(target=annotate_graph, args=(annotation_event, annotation_queue,)).start()
    for fig in figures:
        annotator_object = Annotator(fig, annotation_event, annotation_queue)
        fig.canvas.mpl_connect("button_press_event", annotator_object.add_note)
        fig.canvas.mpl_connect("pick_event", annotator_object.on_pick)
        fig.canvas.mpl_connect("button_release_event", annotator_object.on_release)
        fig.canvas.mpl_connect("key_press_event", annotator_object.on_key_press)
        fig.canvas.mpl_connect("key_release_event", annotator_object.on_key_release)
        list_of_annotators.append(annotator_object)  # do this to prevent garbage collection
    return list_of_annotators


def redraw_annotations(list_of_annotators, redraw_canvas=False):
    for obj in list_of_annotators:
        obj.redraw_annotations(redraw_canvas=redraw_canvas)


def get_annotations(list_of_annotators):
    annotations_dict = {}
    for i, obj in enumerate(list_of_annotators):
        annotations_dict[i] = obj.get_annotations()
    return annotations_dict


def put_annotations(data: dict, list_of_annotators: list):
    for key, values in data.items():
        for sub_key, sub_values in values.items():
            note_text = sub_values["note_text"]
            offset_text = sub_values["offset_text"]
            picker_value = sub_values["picker_value"]
            data_point = sub_values["data_point"]
            subplot_number = sub_values["subplot_number"]
            list_of_annotators[int(key)].put_annotations(note_text, offset_text, picker_value, data_point, subplot_number)


class EditAnnotation:
    """ Helper Class for Annotator Class """

    def __init__(self, root, parent, title=None, initial_value=""):
        self.root = tkb.Toplevel(master=root, topmost=True)
        self.initial_value = initial_value
        self.result = None

        if title:
            self.root.title(title)

        self.body(self.root)
        self.buttonbox()
        self.root.wait_window(self.root)  # Wait for the window to be closed

    def body(self, parent):
        # self.attributes("-topmost", True)  # bring widget to the front
        tk.Label(parent, text="Edit annotation:").grid(row=0)
        self.text = tk.Text(parent, width=25, height=5)
        self.text.insert("1.0", self.initial_value)
        self.text.grid(row=1)
        return self.text

    def buttonbox(self, edit=True):
        box = tk.Frame(self.root)
        tk.Button(box, text="OK", width=10, command=self.ok, default="active").pack(side="left", padx=5, pady=5)
        tk.Button(box, text=f"Delete", width=10, command=self.cancel).pack(side="left", padx=5, pady=5)
        box.grid(row=2)

    def apply(self):
        self.result = self.text.get("1.0", "end-1c")  # "end-1c" gets rid of the extra newline

    def ok(self):
        self.apply()
        self.root.destroy()

    def cancel(self):
        self.root.destroy()


class CreateAnnotation:
    """ Helper Class for Annotator Class """

    def __init__(self, root, parent, title=None, initial_value=""):
        self.root = tkb.Toplevel(master=root, topmost=True)
        self.initial_value = initial_value
        self.result = None

        if title:
            self.root.title(title)

        self.body(self.root)
        self.buttonbox()
        self.root.wait_window(self.root)  # Wait for the window to be closed

    def body(self, parent):
        # self.attributes("-topmost", True)  # bring widget to the front
        tk.Label(parent, text="Enter annotation:").grid(row=0)
        self.text = tk.Text(parent, width=25, height=5)
        self.text.insert("1.0", self.initial_value)
        self.text.grid(row=1)
        return self.text

    def buttonbox(self, edit=True):
        box = tk.Frame(self.root)
        tk.Button(box, text="OK", width=10, command=self.ok, default="active").pack(side="left", padx=5, pady=5)
        tk.Button(box, text=f"Cancel", width=10, command=self.cancel).pack(side="left", padx=5, pady=5)
        box.grid(row=2)

    def apply(self):
        self.result = self.text.get("1.0", "end-1c")  # "end-1c" gets rid of the extra newline

    def ok(self):
        self.apply()
        self.root.destroy()

    def cancel(self):
        self.root.destroy()


class Annotator:
    def __init__(self, figure, annotation_event, annotation_queue):
        self.figure = figure
        self.axes = None
        self.annotations = []
        self.selected_annotation = None
        self.ctrl_pressed = False
        self.currently_open = False
        self.annotation_event = annotation_event
        self.annotation_queue = annotation_queue

    def get_dialog_text(self, initial_value, edit):
        dialog_dict = {"value": initial_value, "edit": edit}
        self.annotation_queue.put(dialog_dict)  # put data into the queue
        self.annotation_event.clear()
        # # wait until there is a response
        self.annotation_event.wait()

        dialog_text = self.annotation_queue.get()['value']  # get data from the queue

        return dialog_text

    def put_annotations(self, note_text, offset_text, picker_value, data_point, subplot_number):
        new_axis = self.get_axis_by_subplot_number(subplot_number)
        if new_axis is None:
            print(f"Warning: No axis found for subplot number {subplot_number}. Skipping and Deleting annotation.")
        else:
            # Redraw the annotation with the same properties
            new_annotation = new_axis.annotate(
                note_text,
                data_point,
                xytext=offset_text,  # Make sure this is set to the correct value (new_x, new_y)
                textcoords='data',  # Use 'data' as in the original annotation
                arrowprops=dict(facecolor='black', arrowstyle="->")
            )

            new_annotation.data_point = data_point
            new_annotation.set_picker(picker_value)

            # Add the new annotation to the new list
            self.annotations.append(new_annotation)

    def get_annotations(self):
        annotation_dict = {}
        for annotation in self.annotations:
            # Get the text of the annotation
            note_text = annotation.get_text()
            offset_text = annotation.get_position()
            picker_value = annotation.get_picker()
            data_point = annotation.data_point
            axis = annotation.axes
            subplot_number = self.get_subplot_number(axis)

            annotation_dict[subplot_number] = {"note_text": note_text, "offset_text": offset_text, "picker_value":
                picker_value, "data_point": data_point, "subplot_number": subplot_number}
        return annotation_dict

    def get_axis_by_subplot_number(self, subplot_number):
        """ Helper method for redraw annotations. """
        # Get all axes in the figure
        all_axes = self.figure.get_axes()
        # Filter out secondary axes
        primary_axes = []
        for ax in all_axes:
            primary_ax = ax.get_shared_x_axes().get_siblings(ax)[0]
            if primary_ax not in primary_axes:
                primary_axes.append(primary_ax)

        # return the new axis at the same subplot number, or return None if it doesn't exist anymore
        if subplot_number < len(primary_axes):
            return primary_axes[subplot_number]
        else:
            return None

    @staticmethod
    def get_subplot_number(axis):
        """ Helper method for redraw annotations. """
        subplot_spec = axis.get_subplotspec()
        grid_spec = subplot_spec.get_gridspec()
        num_rows, num_columns = grid_spec.get_geometry()
        row, col = subplot_spec.rowspan.start, subplot_spec.colspan.start
        subplot_number = row * num_columns + col
        return subplot_number

    def redraw_annotations(self, redraw_canvas=False):
        # List to hold the newly created annotations
        new_annotations = []

        # Iterate through the existing annotations
        for annotation in self.annotations:
            # Extract the properties
            note_text = annotation.get_text()
            offset_text = annotation.get_position()
            picker_value = annotation.get_picker()
            data_point = annotation.data_point
            axis = annotation.axes
            subplot_number = self.get_subplot_number(axis)

            # Remove the existing annotation
            annotation.remove()

            new_axis = self.get_axis_by_subplot_number(subplot_number)
            if new_axis is None:
                print(f"Warning: No axis found for subplot number {subplot_number}. Skipping and Deleting annotation.")
                continue
            # Redraw the annotation with the same properties
            new_annotation = new_axis.annotate(
                note_text,
                data_point,
                xytext=offset_text,  # Make sure this is set to the correct value (new_x, new_y)
                textcoords='data',  # Use 'data' as in the original annotation
                arrowprops=dict(facecolor='black', arrowstyle="->")
            )

            new_annotation.data_point = data_point
            new_annotation.set_picker(picker_value)

            # Add the new annotation to the new list
            new_annotations.append(new_annotation)

        # Replace the old annotations list with the new one
        self.annotations = new_annotations

        # Redraw the figure to make the changes visible
        if redraw_canvas:
            self.figure.canvas.draw_idle()

    def add_note(self, event):
        if not self.currently_open:
            self.axes = self.figure.get_axes()  # get all axes
            if event.inaxes in self.axes:
                if event.dblclick:  # Right double click
                    self.currently_open = True
                    for annotation in self.annotations:
                        contains, _ = annotation.contains(event)
                        if contains:
                            self.edit_or_delete_annotation(annotation)
                            self.currently_open = False
                            return
                    selected_x, selected_y = event.xdata, event.ydata
                    initial_value = f"(x={selected_x:.4f}, y={selected_y:.4f})"
                    note_text = self.get_dialog_text(initial_value, edit=False)
                    if note_text is not None:
                        annotation = event.inaxes.annotate(note_text, (selected_x, selected_y), textcoords="data",
                                                           xytext=(selected_x, selected_y), arrowprops=dict(facecolor='black', arrowstyle="->"))
                        annotation.set_picker(5)
                        annotation.data_point = (selected_x, selected_y)  # Save the original data point
                        self.annotations.append(annotation)
                        plt.draw()
                    self.currently_open = False
        else:
            print("You already have a dialog box open!")

    def edit_or_delete_annotation(self, annotation):
        new_text = self.get_dialog_text(initial_value=annotation.get_text(), edit=True)

        if new_text is not None:
            # update the text
            annotation.set_text(new_text)
            plt.draw()
        else:
            # if user cancels (provides no input), delete the annotation
            annotation.remove()
            try:
                self.annotations.remove(annotation)
            except Exception:
                print("There was no annotation to remove!")
            plt.draw()

    def on_pick(self, event):
        if self.ctrl_pressed:
            self.selected_annotation = event.artist

    def on_release(self, event):
        try:
            if self.selected_annotation is not None:
                new_x, new_y = event.xdata, event.ydata
                if new_x is not None and new_y is not None:
                    ax = self.selected_annotation.axes  # Store the axes before removing the annotation

                    # Remove the old annotation
                    self.selected_annotation.remove()
                    self.annotations.remove(self.selected_annotation)

                    # Create a new annotation at the new location with an arrow pointing to the original data point
                    new_annotation = ax.annotate(self.selected_annotation.get_text(), self.selected_annotation.data_point,
                                                 xytext=(new_x, new_y), textcoords='data',
                                                 arrowprops=dict(facecolor='black', arrowstyle="->"))
                    new_annotation.set_picker(5)
                    new_annotation.data_point = self.selected_annotation.data_point
                    self.annotations.append(new_annotation)
                    self.selected_annotation = None
                    plt.draw()
        except Exception as e:
            print(e)

    def on_key_press(self, event):
        if event.key == 'control':
            self.ctrl_pressed = True

    def on_key_release(self, event):
        if event.key == 'control':
            self.ctrl_pressed = False


if __name__ == '__main__':
    pass
