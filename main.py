import tkinter as tk
import tkinter.ttk as ttk

from src.utils_gui import (
    WINDOW_TITLE,
    WIDTH_WINDOW,
    HEIGHT_WINDOW,
)

# class SubMenuField -> Menu on hover for fields.
# class Console -> Console 
# class MenuOutput -> Show raw expected output for what will be generated, allow scrolling

class ReferenceFields(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title(WINDOW_TITLE)
        self.geometry(f'{WIDTH_WINDOW}x{HEIGHT_WINDOW}')


def main():
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()
