from model.canvas import Canvas
from model.shape_factory import ShapeFactory

class CanvasController:
    def __init__(self, canvas_view, property_panel):
        self.canvas = Canvas()
        self.canvas_view = canvas_view
        self.property_panel = property_panel
        
        self.canvas.add_observer(self)
        self.canvas_view.set_shape_selected_callback(self.on_canvas_click)
        self.canvas_view.set_shape_created_callback(self.on_shape_created)
        self.property_panel.set_property_changed_callback(self.on_property_changed)
    
    def on_canvas_click(self, x: int, y: int, multi_select: bool = False):
        clicked_shape = None
        for shape in reversed(self.canvas.get_shapes()):
            if (shape.x <= x <= shape.x + shape.width and
                shape.y <= y <= shape.y + shape.height):
                clicked_shape = shape
                break
        
        if clicked_shape:
            if multi_select:
                # Add to or remove from selection
                if clicked_shape in self.canvas.selected_shapes:
                    self.canvas.selected_shapes.remove(clicked_shape)
                    clicked_shape.selected = False
                else:
                    self.canvas.selected_shapes.append(clicked_shape)
                    clicked_shape.selected = True
                self.canvas.notify_observers()
            else:
                # Single selection
                self.canvas.select_shapes([clicked_shape])
            
            if len(self.canvas.selected_shapes) == 1:
                self.property_panel.update_properties(clicked_shape.draw())
            elif len(self.canvas.selected_shapes) > 1:
                # Show common properties for multiple selected shapes
                self.property_panel.show_multi_select_properties()
        elif not multi_select:
            self.canvas.select_shapes([])
            self.property_panel.clear_properties()
    
    def on_shape_created(self, x: int, y: int, width: int, height: int, shape_type: str = "rectangle"):
        shape = ShapeFactory.create_shape(shape_type)
        shape.x = x
        shape.y = y
        if shape_type == "line":
            shape.x2 = width  # width parameter is actually x2 for lines
            shape.y2 = height  # height parameter is actually y2 for lines
        else:
            shape.width = width
            shape.height = height
        self.canvas.add_shape(shape)
    
    def on_property_changed(self, property_name: str, value: any):
        for shape in self.canvas.selected_shapes:
            if property_name in ['x', 'y', 'width', 'height', 'z_order']:
                try:
                    value = int(value)
                except ValueError:
                    return
            shape.set_property(property_name, value)
        self.canvas.notify_observers()
    
    def update(self):
        self.canvas_view.draw_shapes(self.canvas.get_shapes()) 