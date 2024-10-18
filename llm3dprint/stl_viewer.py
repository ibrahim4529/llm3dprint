from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyvista as pv
from pyvistaqt import BackgroundPlotter


class STLViewer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter = BackgroundPlotter(show=False)
        self.plotter.add_mesh(pv.Sphere())
        layout.addWidget(self.plotter.interactor)
        self.setLayout(layout)
        self.plotter.show()

    def load_stl(self, stl_path):
        self.plotter.clear()
        self.plotter.add_mesh(pv.read(stl_path))
        self.plotter.show()