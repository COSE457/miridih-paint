from abc import ABC, abstractmethod
from typing import Dict

class Shape(ABC):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 100
        self.text = ""
        self.z_order = 0
        self.has_frame = False
        self.has_shadow = False
        self.selected = False
        self.fill = ""
        self.outline = "black"
        
    @abstractmethod
    def draw(self) -> Dict:
        pass
    
    def set_property(self, name: str, value: any) -> None:
        if hasattr(self, name):
            setattr(self, name, value)
    
    def get_property(self, name: str) -> any:
        return getattr(self, name, None)
    
    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
    
    def resize(self, dw: int, dh: int) -> None:
        self.width = max(10, self.width + dw)
        self.height = max(10, self.height + dh)

class Rectangle(Shape):
    def __init__(self):
        super().__init__()
        self.shape_type = "rectangle"
        
    def draw(self) -> Dict:
        return {
            'type': self.shape_type,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'text': self.text,
            'z_order': self.z_order,
            'has_frame': self.has_frame,
            'has_shadow': self.has_shadow,
            'selected': self.selected,
            'fill': self.fill,
            'outline': self.outline
        }

class Ellipse(Shape):
    def __init__(self):
        super().__init__()
        self.shape_type = "ellipse"
        
    def draw(self) -> Dict:
        return {
            'type': self.shape_type,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'text': self.text,
            'z_order': self.z_order,
            'has_frame': self.has_frame,
            'has_shadow': self.has_shadow,
            'selected': self.selected,
            'fill': self.fill,
            'outline': self.outline
        }

class Line(Shape):
    def __init__(self):
        super().__init__()
        self.shape_type = "line"
        self.x2 = 0  # End point x
        self.y2 = 0  # End point y
        self.width = 1  # Line width
        
    def draw(self) -> Dict:
        return {
            'type': self.shape_type,
            'x': self.x,
            'y': self.y,
            'x2': self.x2,
            'y2': self.y2,
            'width': self.width,
            'z_order': self.z_order,
            'selected': self.selected,
            'outline': self.outline
        }
        
    def resize(self, dw: int, dh: int) -> None:
        self.x2 += dw
        self.y2 += dh

class Text(Shape):
    def __init__(self):
        super().__init__()
        self.shape_type = "text"
        self.font = "Arial"
        self.font_size = 12
        self.text_color = "black"
        
    def draw(self) -> Dict:
        return {
            'type': self.shape_type,
            'x': self.x,
            'y': self.y,
            'text': self.text,
            'font': self.font,
            'font_size': self.font_size,
            'text_color': self.text_color,
            'z_order': self.z_order,
            'selected': self.selected
        }

class Image(Shape):
    def __init__(self):
        super().__init__()
        self.shape_type = "image"
        self.image_path = ""
        self.preserve_aspect_ratio = True
        
    def draw(self) -> Dict:
        return {
            'type': self.shape_type,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'image_path': self.image_path,
            'preserve_aspect_ratio': self.preserve_aspect_ratio,
            'z_order': self.z_order,
            'has_frame': self.has_frame,
            'has_shadow': self.has_shadow,
            'selected': self.selected
        } 