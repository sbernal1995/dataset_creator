# src/widgets/autocomplete_line_edit.py
from PyQt5.QtWidgets import QLineEdit, QCompleter
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter

class AutoCompleteLineEdit(QLineEdit):
    """
    QLineEdit personalizado que muestra:
      - Un popup con las opciones del QCompleter.
      - La sugerencia inline en gris, es decir, la parte completada del texto.
      - Permite iterar entre sugerencias con la tecla TAB.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._completer = None
        self._suggestion = ""
        self.textChanged.connect(self.updateSuggestion)

    def setCompleter(self, completer: QCompleter):
        self._completer = completer
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        super().setCompleter(completer)

    def updateSuggestion(self, text):
        """Busca la mejor sugerencia que empiece con el texto actual."""
        self._suggestion = ""
        if self._completer is not None and text:
            model = self._completer.completionModel()
            # Se busca la primera coincidencia que empiece con el texto (sin distinguir mayúsculas)
            for row in range(model.rowCount()):
                idx = model.index(row, 0)
                candidate = model.data(idx)
                if candidate.lower().startswith(text.lower()):
                    self._suggestion = candidate
                    break
        self.update()  # Repinta el widget para mostrar la sugerencia

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            current_text = self.text()
            if self._suggestion and len(self._suggestion) > len(current_text):
                self.setText(self._suggestion)
                self.setCursorPosition(len(self._suggestion))
                event.accept()
                return
        super().keyPressEvent(event)

    def focusNextPrevChild(self, next):
        return False

    def paintEvent(self, event):
        """
        Dibuja el QLineEdit y, si existe una sugerencia que extienda el texto actual,
        dibuja la parte faltante en color gris.
        """
        super().paintEvent(event)
        current_text = self.text()
        if self._suggestion and current_text and len(self._suggestion) > len(current_text):
            # Calcular el ancho del texto actual
            fm = self.fontMetrics()
            text_width = fm.width(current_text)
            painter = QPainter(self)
            painter.setPen(Qt.gray)
            # Calcular la posición en base a los márgenes del QLineEdit
            x = self.contentsRect().left() + text_width + 2  # +2 para un pequeño margen
            # La posición vertical se alinea con la línea base del texto
            y = self.contentsRect().bottom() - fm.descent()
            # Dibujar la parte de la sugerencia que falta
            remaining = self._suggestion[len(current_text):]
            painter.drawText(x, y, remaining)
