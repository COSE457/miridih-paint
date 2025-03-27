import tkinter as tk
from tkinter import ttk
from .canvas_view import CanvasView
from .property_panel import PropertyPanel

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Miridih Paint")
        
        # Create menu bar
        self.create_menu()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas view
        self.canvas_view = CanvasView(self.main_frame)
        self.canvas_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create property panel
        self.property_panel = PropertyPanel(self.main_frame)
        self.property_panel.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Delete")
    
    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=2)
        
        # Shape selection
        ttk.Label(toolbar, text="Shape:").pack(side=tk.LEFT, padx=5)
        shapes = ["Rectangle", "Ellipse", "Line", "Text", "Image"]
        shape_var = tk.StringVar(value="Rectangle")
        shape_menu = ttk.OptionMenu(
            toolbar, shape_var, "Rectangle", *shapes,
            command=lambda x: self.canvas_view.set_shape_type(x.lower())
        )
        shape_menu.pack(side=tk.LEFT, padx=5)
    
    def start(self):
        self.root.mainloop() 