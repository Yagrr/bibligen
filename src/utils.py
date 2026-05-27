import os

import tkinter as tk
import ttkbootstrap as ttk

# Create scrollbar for input frame
class ScrollBar:
    """
        Scrollbar UI object. Pass a `parent` container Frame and a target
        canvas that has its parent also set as the `parent`.
        Objects are to be drawn inside the canvas.
    """
    def __init__(self, parent: ttk.Frame, target_canvas: ttk.Canvas):
        self.parent = parent
        self.ui_canvas = target_canvas
        self.gui_setup_scrollbar()

    def gui_setup_scrollbar(self):
        """ 
        Create scrollable frame with ui_canvas to contain field entries.
        This is needed as different document types will have different numbers
        of fields.
        """
        self.ui_scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.ui_canvas.yview)
        self.ui_canvas.configure(yscrollcommand=self.ui_scrollbar.set)

        self.ui_scrollable_frame = ttk.Frame(self.parent)

        self.ui_canvas.pack(side="left", fill="both", expand=True)
        self.ui_scrollbar.pack(side="right", fill="y")

        self.ui_canvas_window = self.ui_canvas.create_window((0, 0), window=self.ui_scrollable_frame, anchor="nw")
        # Bind controls for scrolling
        self.ui_scrollable_frame.bind("<Configure>", self.scroll_on_frame_configure)
        self.ui_canvas.bind("<Configure>", self.scroll_on_canvas_configure)
        
    # Functions on_frame_configure and on_canvas_configure used for scrolling
    def scroll_on_frame_configure(self, event):
        self.ui_canvas.configure(scrollregion=self.ui_canvas.bbox("all"))

    def scroll_on_canvas_configure(self, event):
        canvas_width = event.width
        self.ui_canvas.itemconfig(self.ui_canvas_window, width=canvas_width)

def _debug_log_fn_decorator(fn):
    """
    Function wrapper for logging when a function is called.
    Usage: Decorate function with @_debug_log and pass logging level from the
    `logging` module (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    def _debug_log_fn_wrapper(*args, **kwargs):
        import inspect
        import logging

        PATH_SRC = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        PATH_LOG = os.path.join(PATH_SRC, ".debug.log")
        logging.basicConfig(
            filename=PATH_LOG,
            filemode="a",
            format="%(asctime)s %(message)s",
            datefmt="%m/%d%Y %I:%M:%S %p",
            encoding="utf-8",
            level=logging.DEBUG,
        )
        logging.info(f"Calling {fn.__name__}\n args: {args}\n kwargs: {kwargs}\n members:{inspect.getmembers(fn)}")
        fn_result = fn(*args, **kwargs)
        logging.info(f"return: {fn_result}")
        return fn_result
    return _debug_log_fn_wrapper
