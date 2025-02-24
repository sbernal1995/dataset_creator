# src/dialogs/help_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt


class HelpDialog(QDialog):
    """
    Diálogo que muestra instrucciones detalladas y visualmente resaltadas para el uso de Video Annotator.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Instrucciones de uso")
        self.setModal(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Instrucciones formateadas en HTML para destacar atajos y comandos clave
        instructions = """
        <h2>Instrucciones</h2>
        <p>
            <b>Abrir Video:</b> Selecciona <i>"File &gt; Abrir video"</i> para cargar un video en formatos 
            <code>.mp4</code>, <code>.avi</code> o <code>.mkv</code>. El diálogo recordará la carpeta del último video abierto.
        </p>
        <p>
            <b>Reproducción:</b> El video comienza a reproducirse automáticamente. Utiliza los siguientes atajos:
            <ul>
                <li><b>Barra espaciadora</b>: Alterna entre reproducir y pausar.</li>
                <li><b>Flecha Izquierda</b>: Retrocede 5 segundos.</li>
                <li><b>Flecha Derecha</b>: Avanza 5 segundos.</li>
            </ul>
        </p>
        <p>
            <b>Modo Anotación:</b> Al pausar el video se captura el frame actual y se activa un overlay para anotar.
            <br>
            <u>Pasos para anotar:</u>
            <ol>
                <li>Dibuja un rectángulo sobre el área de interés.</li>
                <li>Al soltar el click, se abre un cuadro de diálogo para seleccionar la especie.</li>
                <li>
                    En el diálogo, escribe la especie. Se desplegará una lista de sugerencias que se completan en gris.
                    <br>
                    <b>Atajo:</b> Presiona <code>TAB</code> para aceptar la sugerencia mostrada.
                </li>
                <li>Al activar la opción <b>"Recordar especie"</b>, el campo se pre-cargará en futuras anotaciones.</li>
            </ol>
        </p>
        <p>
            <b>Recordar Especie:</b> En el diálogo de selección, activa o desactiva el checkbox <i>"Recordar especie"</i>.
            <br>
            Si está activado, se pre-cargará el último valor seleccionado; de lo contrario, el campo estará vacío.
        </p>
        <p>
            <b>Visualización:</b> 
            <br>
            - La sugerencia gris se muestra a medida que se escribe.
            <br>
            - El popup desplegable muestra todas las coincidencias disponibles.
        </p>
        <p>
            Si necesitas revisar estas instrucciones nuevamente, selecciona <i>"Ayuda &gt; Instrucciones"</i> en el menú.
        </p>
        """
        label = QLabel(instructions)
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        layout.addWidget(label)

        close_button = QPushButton("Cerrar", self)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)
