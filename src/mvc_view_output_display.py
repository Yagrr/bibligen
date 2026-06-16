import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText


class WrapperOutputWindow(ttk.Frame):
    """
    Parent GUI Frame container that contains the window for the output window.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.output_window = ViewOutputWindow(self)
        self.output_window.pack(expand=True, fill=tk.BOTH)


class ViewOutputWindow(ScrolledText):
    def __init__(self, container=None, **kw):
        ScrolledText.__init__(self, container, **kw)
        self.parent = container
        self.text["state"] = "disabled"

        test = []
        for i in range(50):
            test.append("hello\n")
        self.set_output_text("".join(test))

    def set_output_text(self, text: str) -> None:
        self.text["state"] = "normal"
        self.text.delete("1.0", tk.END)
        self.text.insert(index="1.0", chars=text)
        self.text["state"] = "disabled"

    def clear_text(self) -> None:
        self.text.delete("1.0", tk.END)
