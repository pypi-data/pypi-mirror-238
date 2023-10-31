import matplotlib.pyplot as plt
from io import BytesIO
import win32clipboard
from PIL import Image
import matplotlib
import os


def copy_axis_to_clipboard(figures: list):
    for fig in figures:
        fig.canvas.mpl_connect('button_press_event', lambda x: save_and_copy_to_clipboard(x))


def copy_to_clipboard(filepath):
    """ Copies the Image in the save location to the Clipboard """
    image = Image.open(filepath)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    # Send to Clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def save_and_copy_to_clipboard(event, dpi=300):
    """
    Save the current plot to a temporary file and copy it to the clipboard on a right-click event.

    Parameters
    ----------
    event : matplotlib.backend_bases.MouseEvent
        The MouseEvent object for the click event.
    dpi : int, optional, default: 300
        The resolution of the saved image in dots per inch.
    """
    if event.button == 3:
        ax = event.inaxes
        if ax is not None:
            shared_axes = ax.get_shared_x_axes().get_siblings(ax)
            # NEW WAY
            if len(shared_axes) == 2:
                save_to_new_figure(shared_axes[1], shared_axes[0])
            else:
                save_to_new_figure(ax)

            print(f"Saved image to temp_image.png")
            copy_to_clipboard('temp_image.png')
            print("File Copied to Clipboard")
            # Check if the file exists before deleting
            if os.path.exists('temp_image.png'):
                os.remove('temp_image.png')
            print("Deleted temp_image.png")
    else:
        pass


def save_to_new_figure(ax1, twinx1=None):
    """
    Save the given axis and its twin axis, if present, to a new figure and export as an image file.

    Parameters
    ----------
    ax1 : matplotlib.axes.Axes
        The main axis to be saved.
    twinx1 : matplotlib.axes.Axes, optional, default: None
        The twin axis (shared x-axis) to be saved, if present.
    """
    # Create the second figure and copy the axis from the first figure
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.set_title(ax1.get_title())
    # Create a twin axis if it exists
    if twinx1:
        twinx2 = ax2.twinx()

        for line in ax1.get_lines():
            ax2.plot(line.get_xdata(), line.get_ydata(),
                     color=line.get_color(),
                     linestyle=line.get_linestyle(),
                     linewidth=line.get_linewidth(),
                     marker=line.get_marker(),
                     markersize=line.get_markersize(),
                     markerfacecolor=line.get_markerfacecolor(),
                     markeredgecolor=line.get_markeredgecolor(),
                     label=line.get_label())
        for line in twinx1.get_lines():
            new_line = plt.Line2D(line.get_xdata(), line.get_ydata(), linestyle=line.get_linestyle(),
                                  linewidth=line.get_linewidth(), color=line.get_color(), marker=line.get_marker(),
                                  markersize=line.get_markersize(), markerfacecolor=line.get_markerfacecolor(),
                                  markeredgecolor=line.get_markeredgecolor(), label=line.get_label())
            twinx2.add_line(new_line)
        for child in twinx1.get_children():
            # print(type(child))
            if isinstance(child, matplotlib.text.Annotation):
                note_text = child.get_text()
                offset_text = child.get_position()
                picker_value = child.get_picker()
                data_point = child.xy

                new_annotation = twinx2.annotate(
                    note_text,
                    data_point,
                    xytext=offset_text,  # Make sure this is set to the correct value (new_x, new_y)
                    textcoords='data',  # Use 'data' as in the original annotation
                    arrowprops=dict(facecolor='black', arrowstyle="->")
                )
                new_annotation.data_point = data_point
                new_annotation.set_picker(picker_value)

        twinx2.set_xlabel(twinx1.get_xlabel())
        twinx2.set_ylabel(twinx1.get_ylabel())
        ax2.set_xlabel(ax1.get_xlabel())
        ax2.set_ylabel(ax1.get_ylabel())

        handles, labels = ax1.get_legend_handles_labels()
        ax2.legend(handles, labels, loc='lower left', bbox_to_anchor=(0, 1.01))
        handles, labels = twinx1.get_legend_handles_labels()
        twinx2.legend(handles, labels, loc='lower right', bbox_to_anchor=(1, 1.01))

        twinx2.set_ylim(twinx1.get_ylim())
        ax2.set_ylim(ax1.get_ylim())
    else:
        # Iterate over each child object in the original axis and recreate it in the new axis
        for child in ax1.get_children():
            # print(type(child))
            if isinstance(child, matplotlib.spines.Spine):
                # Copy the spines
                ax2.spines[child.spine_type].set_visible(child.get_visible())
                ax2.spines[child.spine_type].set_color(child.get_edgecolor())
                ax2.spines[child.spine_type].set_linewidth(child.get_linewidth())

            elif isinstance(child, matplotlib.image.AxesImage):
                # Copy the image
                ax2.imshow(child.get_array())
                ax2.axis('off')

            elif isinstance(child, matplotlib.legend.Legend):
                # Copy the legend
                handles, labels = ax1.get_legend_handles_labels()
                ax2.legend(handles, labels, loc='lower left', bbox_to_anchor=(0, 1.01))

            elif isinstance(child, matplotlib.lines.Line2D):
                ax2.axis('on')
                ax2.set_xlabel(ax1.get_xlabel())
                ax2.set_ylabel(ax1.get_ylabel())
                # Copy the lines
                line = child
                ax2.plot(line.get_xdata(), line.get_ydata(),
                         color=line.get_color(),
                         linestyle=line.get_linestyle(),
                         linewidth=line.get_linewidth(),
                         marker=line.get_marker(),
                         markersize=line.get_markersize(),
                         markerfacecolor=line.get_markerfacecolor(),
                         markeredgecolor=line.get_markeredgecolor(),
                         label=line.get_label())

            elif isinstance(child, matplotlib.patches.Rectangle):
                rect = child
                if rect.get_width() != 1 and rect.get_height() != 1:
                    ax2.axis('off')
                    # Copy the rectangles
                    new_rect = matplotlib.patches.Rectangle((rect.get_xy()), rect.get_width(), rect.get_height(),
                                                            fill=rect.get_fill(),
                                                            facecolor=rect.get_facecolor(),
                                                            edgecolor=rect.get_edgecolor(),
                                                            linewidth=rect.get_linewidth(),
                                                            linestyle=rect.get_linestyle())
                    ax2.add_patch(new_rect)
            elif isinstance(child, matplotlib.text.Text):
                if isinstance(child, matplotlib.text.Annotation):
                    note_text = child.get_text()
                    offset_text = child.get_position()
                    picker_value = child.get_picker()
                    data_point = child.xy

                    new_annotation = ax2.annotate(
                        note_text,
                        data_point,
                        xytext=offset_text,  # Make sure this is set to the correct value (new_x, new_y)
                        textcoords='data',  # Use 'data' as in the original annotation
                        arrowprops=dict(facecolor='black', arrowstyle="->")
                    )
                    new_annotation.data_point = data_point
                    new_annotation.set_picker(picker_value)
                else:
                    # header stuff we don't want to include.
                    if child.get_position()[1] == 1:
                        continue
                    # Copy the text labels
                    text_x, text_y = child.get_position()
                    text_content = child.get_text()
                    text_props = {
                        'fontsize': child.get_fontsize(),
                        'color': child.get_color(),
                        'verticalalignment': child.get_verticalalignment(),
                        'horizontalalignment': child.get_horizontalalignment(),
                        'fontweight': child.get_fontweight(),
                        'fontstyle': child.get_fontstyle(),
                        'fontfamily': child.get_fontfamily(),
                    }
                    ax2.text(text_x, text_y, text_content, **text_props)

            elif isinstance(child, matplotlib.collections.PathCollection):
                # Copy the scatter plot
                offsets = child.get_offsets()
                colors = child.get_facecolor()
                ax2.scatter(offsets[:, 0], offsets[:, 1], c=colors)

    ax2.autoscale_view()
    fig2.tight_layout()
    fig2.canvas.draw()
    fig2.savefig('temp_image.png')


if __name__ == '__main__':
    pass
