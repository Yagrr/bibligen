import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from tkinter.filedialog import asksaveasfile


class WrapperOutputWindow(ttk.Frame):
    """
    Parent GUI Frame container that contains the window for the output window.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.ui_output_window = ViewOutputWindow(self)
        self.ui_output_window.pack(expand=True, fill=tk.BOTH)
        self.ui_save_to_file = ttk.Button(self, width=10, text="Save to file", command=self.show_save_to_file_dialog)
        self.ui_copy_to_clipboard_button = ttk.Button(self, width=5, text="Copy", command=self.copy_to_clipboard)
        self.ui_save_to_file.place(x=110, y=910)
        self.ui_copy_to_clipboard_button.place(x=20, y=910)

    def show_save_to_file_dialog(self) -> None:
        file = asksaveasfile(mode="w", defaultextension=".bib")
        if file is None:
            return
        text_output = self.ui_output_window.text.get("1.0", tk.END)
        file.write(text_output)
        file.close()
        return
        

    def copy_to_clipboard(self) -> None:
        text_output = self.ui_output_window.text.get("1.0", tk.END)

        copy = tk.Tk()
        copy.withdraw()
        copy.clipboard_clear()
        copy.clipboard_append(text_output)
        copy.destroy()
        del copy


class ViewOutputWindow(ScrolledText):
    def __init__(self, container=None, **kw):
        ScrolledText.__init__(self, container, **kw)
        self.parent = container
        self.text["state"] = "disabled"

        self.set_output_text("Click 'Generate entries' to refresh\n")

    def set_output_text(self, text: str) -> None:
        self.text["state"] = "normal"
        self.text.delete("1.0", tk.END)
        self.text.insert(index="1.0", chars=text)
        self.text["state"] = "disabled"

    def clear_text(self) -> None:
        self.text.delete("1.0", tk.END)
