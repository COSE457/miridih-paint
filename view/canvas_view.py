import tkinter as tk
from tkinter import PhotoImage, filedialog
from typing import Callable, Optional, Tuple
import os

class CanvasView(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Control-Button-1>', self.on_multi_select)
        
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.current_shape_type = "rectangle"  # Default shape type
        self.multi_select_mode = False
        
        self.shape_selected_callback = None
        self.shape_created_callback = None
        self.images = {}  # Store PhotoImage objects
    
    def set_shape_type(self, shape_type: str):
        self.current_shape_type = shape_type
        if shape_type == "text":
            self.master.focus_set()  # Set focus to receive text input
        elif shape_type == "image":
            self.prompt_for_image()
    
    def prompt_for_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.gif *.bmp")]
        )
        if file_path:
            if file_path not in self.images:
                try:
                    self.images[file_path] = PhotoImage(file=file_path)
                    return file_path
                except:
                    return None
    
    def on_click(self, event):
        if self.current_shape_type == "text":
            # For text, create immediately on click
            if self.shape_created_callback:
                self.shape_created_callback(event.x, event.y, 100, 30)  # Default text box size
        elif self.current_shape_type == "image":
            # For image, prompt for file and create
            file_path = self.prompt_for_image()
            if file_path and self.shape_created_callback:
                self.shape_created_callback(event.x, event.y, 200, 200)  # Default image size
        else:
            self.start_x = event.x
            self.start_y = event.y
            
            if self.shape_selected_callback:
                self.shape_selected_callback(event.x, event.y)
    
    def on_multi_select(self, event):
        self.multi_select_mode = True
        if self.shape_selected_callback:
            self.shape_selected_callback(event.x, event.y, multi_select=True)
    
    def on_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            self.delete("temp_shape")
            if self.current_shape_type == "line":
                self.create_line(
                    self.start_x, self.start_y, event.x, event.y,
                    fill='black', tags=("temp_shape",)
                )
            elif self.current_shape_type == "rectangle":
                self.create_rectangle(
                    self.start_x, self.start_y, event.x, event.y,
                    outline='black', tags=("temp_shape",)
                )
            elif self.current_shape_type == "ellipse":
                self.create_oval(
                    self.start_x, self.start_y, event.x, event.y,
                    outline='black', tags=("temp_shape",)
                )
    
    def on_release(self, event):
        if self.current_shape_type not in ["text", "image"] and self.start_x is not None and self.start_y is not None:
            if self.shape_created_callback:
                x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
                x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
                
                if self.current_shape_type == "line":
                    self.shape_created_callback(
                        self.start_x, self.start_y,
                        event.x - self.start_x,
                        event.y - self.start_y,
                        shape_type=self.current_shape_type
                    )
                else:
                    self.shape_created_callback(
                        x1, y1, x2-x1, y2-y1,
                        shape_type=self.current_shape_type
                    )
            self.delete("temp_shape")
        self.start_x = None
        self.start_y = None
        self.multi_select_mode = False
    
    def draw_shapes(self, shapes):
        self.delete("all")
        for shape in shapes:
            props = shape.draw()
            outline = 'blue' if props['selected'] else props.get('outline', 'black')
            
            if props['type'] == 'rectangle':
                self._draw_rectangle(props, outline)
            elif props['type'] == 'ellipse':
                self._draw_ellipse(props, outline)
            elif props['type'] == 'line':
                self._draw_line(props, outline)
            elif props['type'] == 'text':
                self._draw_text(props)
            elif props['type'] == 'image':
                self._draw_image(props)
    
    def _draw_rectangle(self, props, outline):
        if props['has_shadow']:
            self.create_rectangle(
                props['x'] + 5, props['y'] + 5,
                props['x'] + props['width'] + 5,
                props['y'] + props['height'] + 5,
                fill='gray', stipple='gray50'
            )
        
        self.create_rectangle(
            props['x'], props['y'],
            props['x'] + props['width'],
            props['y'] + props['height'],
            outline=outline,
            fill=props.get('fill', ''),
            width=2 if props['has_frame'] else 1
        )
        
        if props['text']:
            self._draw_shape_text(props)
    
    def _draw_ellipse(self, props, outline):
        if props['has_shadow']:
            self.create_oval(
                props['x'] + 5, props['y'] + 5,
                props['x'] + props['width'] + 5,
                props['y'] + props['height'] + 5,
                fill='gray', stipple='gray50'
            )
        
        self.create_oval(
            props['x'], props['y'],
            props['x'] + props['width'],
            props['y'] + props['height'],
            outline=outline,
            fill=props.get('fill', ''),
            width=2 if props['has_frame'] else 1
        )
        
        if props['text']:
            self._draw_shape_text(props)
    
    def _draw_line(self, props, outline):
        self.create_line(
            props['x'], props['y'],
            props['x'] + props.get('x2', 0),
            props['y'] + props.get('y2', 0),
            fill=outline,
            width=props.get('width', 1)
        )
    
    def _draw_text(self, props):
        self.create_text(
            props['x'], props['y'],
            text=props['text'],
            font=(props.get('font', 'Arial'), props.get('font_size', 12)),
            fill=props.get('text_color', 'black'),
            anchor='nw'
        )
    
    def _draw_image(self, props):
        if props['image_path'] and os.path.exists(props['image_path']):
            if props['image_path'] not in self.images:
                self.images[props['image_path']] = PhotoImage(file=props['image_path'])
            
            if props['has_shadow']:
                self.create_rectangle(
                    props['x'] + 5, props['y'] + 5,
                    props['x'] + props['width'] + 5,
                    props['y'] + props['height'] + 5,
                    fill='gray', stipple='gray50'
                )
            
            self.create_image(
                props['x'], props['y'],
                image=self.images[props['image_path']],
                anchor='nw'
            )
            
            if props['has_frame']:
                self.create_rectangle(
                    props['x'], props['y'],
                    props['x'] + props['width'],
                    props['y'] + props['height'],
                    outline='black',
                    width=2
                )
    
    def _draw_shape_text(self, props):
        self.create_text(
            props['x'] + props['width']/2,
            props['y'] + props['height']/2,
            text=props['text']
        )
    
    def set_shape_selected_callback(self, callback: Callable):
        self.shape_selected_callback = callback
    
    def set_shape_created_callback(self, callback: Callable):
        self.shape_created_callback = callback 