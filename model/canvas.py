from typing import List, Optional
from .shape import Shape

class Canvas:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.shapes = []
            cls._instance.selected_shapes = []
            cls._instance.observers = []
        return cls._instance
    
    def add_shape(self, shape: Shape) -> None:
        self.shapes.append(shape)
        self.notify_observers()
    
    def remove_shape(self, shape: Shape) -> None:
        if shape in self.shapes:
            self.shapes.remove(shape)
            if shape in self.selected_shapes:
                self.selected_shapes.remove(shape)
            self.notify_observers()
    
    def get_shapes(self) -> List[Shape]:
        return sorted(self.shapes, key=lambda x: x.z_order)
    
    def select_shapes(self, shapes: List[Shape]) -> None:
        for shape in self.selected_shapes:
            shape.selected = False
        self.selected_shapes = shapes
        for shape in shapes:
            shape.selected = True
        self.notify_observers()
    
    def add_observer(self, observer) -> None:
        if observer not in self.observers:
            self.observers.append(observer)
    
    def notify_observers(self) -> None:
        for observer in self.observers:
            observer.update() 