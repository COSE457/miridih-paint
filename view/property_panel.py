import tkinter as tk
from tkinter import ttk

class PropertyPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.property_changed_callback = None
        self.create_widgets()
    
    def create_widgets(self):
        self.properties = {}
        labels = ['X', 'Y', 'Width', 'Height', 'Z-Order', 'Text']
        
        for label in labels:
            frame = ttk.Frame(self)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=label).pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=10)
            entry.pack(side=tk.RIGHT)
            entry.bind('<Return>', lambda e, l=label.lower(): self.on_property_change(l))
            self.properties[label.lower()] = entry
        
        # Checkboxes for frame and shadow
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.frame_var = tk.BooleanVar()
        self.shadow_var = tk.BooleanVar()
        
        ttk.Checkbutton(frame, text="Frame", variable=self.frame_var,
                       command=lambda: self.on_property_change('has_frame')).pack(side=tk.LEFT)
        ttk.Checkbutton(frame, text="Shadow", variable=self.shadow_var,
                       command=lambda: self.on_property_change('has_shadow')).pack(side=tk.RIGHT)
        
        # Style properties
        style_frame = ttk.LabelFrame(self, text="Style")
        style_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Font properties
        font_frame = ttk.Frame(style_frame)
        font_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(font_frame, text="Font:").pack(side=tk.LEFT)
        self.font_var = tk.StringVar(value="Arial")
        fonts = ["Arial", "Times", "Helvetica", "Courier"]
        font_menu = ttk.OptionMenu(
            font_frame, self.font_var, "Arial", *fonts,
            command=lambda x: self.on_property_change('font')
        )
        font_menu.pack(side=tk.RIGHT)
        
        # Font size
        size_frame = ttk.Frame(style_frame)
        size_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(size_frame, text="Size:").pack(side=tk.LEFT)
        self.font_size_var = tk.StringVar(value="12")
        size_entry = ttk.Entry(size_frame, textvariable=self.font_size_var, width=5)
        size_entry.pack(side=tk.RIGHT)
        size_entry.bind('<Return>', lambda e: self.on_property_change('font_size'))
        
        # Colors
        color_frame = ttk.Frame(style_frame)
        color_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(color_frame, text="Color:").pack(side=tk.LEFT)
        self.color_var = tk.StringVar(value="black")
        colors = ["black", "red", "green", "blue", "yellow"]
        color_menu = ttk.OptionMenu(
            color_frame, self.color_var, "black", *colors,
            command=lambda x: self.on_property_change('text_color')
        )
        color_menu.pack(side=tk.RIGHT)
    
    def update_properties(self, properties):
        for key, entry in self.properties.items():
            entry.delete(0, tk.END)
            if key in properties:
                entry.insert(0, str(properties[key]))
        
        self.frame_var.set(properties.get('has_frame', False))
        self.shadow_var.set(properties.get('has_shadow', False))
        
        # Update style properties
        if properties.get('type') == 'text':
            self.font_var.set(properties.get('font', 'Arial'))
            self.font_size_var.set(str(properties.get('font_size', 12)))
            self.color_var.set(properties.get('text_color', 'black'))
    
    def show_multi_select_properties(self):
        # Show only common properties for multiple selected shapes
        for entry in self.properties.values():
            entry.delete(0, tk.END)
            entry.insert(0, "Multiple")
        
        # Keep checkboxes enabled for multi-select
        self.frame_var.set(False)
        self.shadow_var.set(False)
    
    def clear_properties(self):
        for entry in self.properties.values():
            entry.delete(0, tk.END)
        self.frame_var.set(False)
        self.shadow_var.set(False)
        self.font_var.set("Arial")
        self.font_size_var.set("12")
        self.color_var.set("black")
    
    def on_property_change(self, property_name):
        if self.property_changed_callback:
            value = None
            if property_name in ['has_frame', 'has_shadow']:
                value = self.frame_var.get() if property_name == 'has_frame' else self.shadow_var.get()
            elif property_name == 'font':
                value = self.font_var.get()
            elif property_name == 'font_size':
                try:
                    value = int(self.font_size_var.get())
                except ValueError:
                    return
            elif property_name == 'text_color':
                value = self.color_var.get()
            else:
                value = self.properties[property_name].get()
            self.property_changed_callback(property_name, value)
    
    def set_property_changed_callback(self, callback):
        self.property_changed_callback = callback 