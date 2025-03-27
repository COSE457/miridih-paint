from .shape import Rectangle, Ellipse, Line, Text, Image

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str):
        shape_types = {
            "rectangle": Rectangle,
            "ellipse": Ellipse,
            "line": Line,
            "text": Text,
            "image": Image
        }
        
        shape_class = shape_types.get(shape_type.lower())
        if shape_class:
            return shape_class()
        raise ValueError(f"Unknown shape type: {shape_type}") 