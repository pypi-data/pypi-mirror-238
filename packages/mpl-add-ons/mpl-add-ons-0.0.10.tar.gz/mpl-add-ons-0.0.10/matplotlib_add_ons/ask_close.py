import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tkb


class SafeToplevel(tkb.Toplevel):
    def destroy(self):
        try:
            super().destroy()  # Call the original destroy method
        except tk.TclError:
            pass  # Ignore the error


def ask_close(figures: list):
    for fig in figures:
        fig.canvas.manager.window.closeEvent = on_close_event


def on_close_event(event):
    master = tk.Tk()
    master.withdraw()  # Hide the main window
    root = SafeToplevel()
    root.title("Save Report")
    root.bind("<Destroy>", lambda x: close_master(master))

    # # root = tk.Tk()
    root.withdraw()
    result = messagebox.askokcancel("Exit", "Are you sure you want to close this graphing window?")
    if result is True:
        event.accept()
    elif result is False:
        # root.destroy()
        event.ignore()
    root.destroy()


def close_master(master):
    master.destroy()


if __name__ == '__main__':
    pass
