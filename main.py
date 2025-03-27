import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from view.main_window import MainWindow
from controller.canvas_controller import CanvasController

def main():
    window = MainWindow()
    controller = CanvasController(window.canvas_view, window.property_panel)
    window.start()

if __name__ == "__main__":
    main() 