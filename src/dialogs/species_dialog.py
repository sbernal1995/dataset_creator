# src/dialogs/species_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QCompleter, QCheckBox
from PyQt5.QtCore import Qt
from src.widgets.autocomplete_line_edit import AutoCompleteLineEdit

class SpeciesDialog(QDialog):
    """
    Diálogo para seleccionar una especie con autocompletar.
    Incluye una opción para recordar la última especie seleccionada.
    """
    # Variables de clase para recordar la última especie y el estado del checkbox
    last_species = ""
    remember_species = True

    def __init__(self, species_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Especie")
        self.species = None

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Nombre de la especie:"))

        # Usar el QLineEdit personalizado para autocompletar
        self.line_edit = AutoCompleteLineEdit(self)
        # Configurar el QCompleter
        completer = QCompleter(species_list, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        try:
            completer.setFilterMode(Qt.MatchContains)
        except Exception:
            pass
        self.line_edit.setCompleter(completer)

        # Agregar checkbox para "Recordar especie" y cargar el estado almacenado
        self.remember_checkbox = QCheckBox("Recordar especie", self)
        self.remember_checkbox.setChecked(SpeciesDialog.remember_species)

        # Si se recuerda la última especie y existe, pre-cargar el campo
        if self.remember_checkbox.isChecked() and SpeciesDialog.last_species:
            self.line_edit.setText(SpeciesDialog.last_species)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.remember_checkbox)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        # Permitir aceptar el diálogo al presionar Enter
        self.line_edit.returnPressed.connect(self.accept)

    def accept(self):
        text = self.line_edit.text().strip()
        if text:
            self.species = text
            # Actualiza last_species según el estado del checkbox
            if self.remember_checkbox.isChecked():
                SpeciesDialog.last_species = text
            else:
                SpeciesDialog.last_species = ""
        # Guarda el estado actual del checkbox para la próxima instancia
        SpeciesDialog.remember_species = self.remember_checkbox.isChecked()
        super().accept()
