# annotation.py
from PyQt5.QtWidgets import QWidget, QInputDialog
from PyQt5.QtCore import Qt, QRect, pyqtSignal


class AnnotationWidget(QWidget):
    # Señal para indicar que se completó una anotación: enviará el nombre de la especie y el bounding box
    annotationCompleted = pyqtSignal(str, QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.drawing = False
        self.start_point = None
        self.end_point = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_point = event.pos()
            self.end_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            self.end_point = event.pos()
            bounding_box = QRect(self.start_point, self.end_point)
            self.prompt_species(bounding_box)

    def prompt_species(self, bounding_box):
        especies = ["Delfín", "Tiburón", "Pez payaso"]
        especie, ok = QInputDialog.getItem(self, "Seleccionar Especie", "Nombre de la especie:", especies, 0, False)
        if ok and especie:
            print("Anotación completada:", especie, bounding_box.getRect())
            self.annotationCompleted.emit(especie, bounding_box)
