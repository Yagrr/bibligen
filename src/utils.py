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
