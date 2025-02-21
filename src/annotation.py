from PyQt5.QtWidgets import QWidget, QInputDialog
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QPixmap

class AnnotationWidget(QWidget):
    # Señal para indicar que se completó una anotación individual
    annotationCompleted = pyqtSignal(str, QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.background_pixmap = None  # Imagen de fondo (snapshot)
        # Lista de anotaciones: cada elemento es una tupla (especie, QRect)
        self.annotations = []

    def setBackground(self, pixmap: QPixmap):
        self.background_pixmap = pixmap
        self.update()

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
            bounding_box = QRect(self.start_point, self.end_point).normalized()
            self.prompt_species(bounding_box)

    def prompt_species(self, bounding_box):
        especies = ["Delfín", "Tiburón", "Pez payaso"]
        especie, ok = QInputDialog.getItem(self, "Seleccionar Especie", "Nombre de la especie:", especies, 0, False)
        if ok and especie:
            # Agregar la anotación a la lista
            self.annotations.append((especie, bounding_box))
            print("Anotación completada:", especie, bounding_box.getRect())
            self.annotationCompleted.emit(especie, bounding_box)
            self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.background_pixmap:
            painter.drawPixmap(self.rect(), self.background_pixmap)
        # Configurar el lápiz para el dibujo
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        painter.setPen(pen)
        # Dibujar todas las anotaciones almacenadas
        for especie, rect in self.annotations:
            painter.drawRect(rect)
        # Si se está dibujando actualmente, mostrar el rectángulo en curso
        if self.drawing and self.start_point and self.end_point:
            current_rect = QRect(self.start_point, self.end_point).normalized()
            painter.drawRect(current_rect)
