import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QSlider, QAction, QFileDialog,
                             QComboBox, QLabel, QStackedLayout)
from PyQt5.QtCore import Qt, QTime

from src.annotation import AnnotationWidget
from video_player import VideoPlayer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reproductor de Video")
        self.setGeometry(100, 100, 800, 600)
        self.create_menu()
        self.setFocusPolicy(Qt.StrongFocus)
        self.total_duration = 0

        # Configuración del widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Contenedor para el video y el overlay de anotación mediante QStackedLayout
        video_container = QWidget()
        self.stack_layout = QStackedLayout(video_container)
        # Permite mostrar todos los widgets apilados (video y anotación) al mismo tiempo
        self.stack_layout.setStackingMode(QStackedLayout.StackAll)

        # Inicializar el reproductor de video y desactivar la ventana nativa para permitir superposición
        self.video_player = VideoPlayer()
        self.video_player.video_widget.setAttribute(Qt.WA_NativeWindow, False)
        self.stack_layout.addWidget(self.video_player.video_widget)

        # Inicializar el widget de anotación y agregarlo al contenedor
        self.annotation_widget = AnnotationWidget(video_container)
        # Se ajusta al tamaño del video; se mostrará solo al pausar
        self.annotation_widget.setGeometry(self.video_player.video_widget.rect())
        self.annotation_widget.hide()
        # Conecta la señal para procesar cada anotación realizada
        self.annotation_widget.annotationCompleted.connect(self.process_annotation)
        self.stack_layout.addWidget(self.annotation_widget)

        # Agregar el contenedor de video/anotación al layout principal
        main_layout.addWidget(video_container)

        # Configurar los controles de reproducción debajo del video
        self.setup_controls(main_layout)

        # Conectar señales del reproductor para actualizar la barra de posición y la duración
        self.video_player.mediaPlayer.positionChanged.connect(self.update_position)
        self.video_player.mediaPlayer.durationChanged.connect(self.update_duration)

    def create_menu(self):
        """Crea el menú de la aplicación con la opción de abrir video."""
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        open_action = QAction("Abrir video", self)
        open_action.triggered.connect(self.open_video)
        file_menu.addAction(open_action)

    def setup_controls(self, parent_layout):
        """Configura los controles de reproducción y los agrega al layout."""
        control_layout = QHBoxLayout()

        # Botón de Play/Pausa
        self.play_pause_button = QPushButton("Pausar")
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        control_layout.addWidget(self.play_pause_button)

        # Slider para controlar la posición del video
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.video_player.set_position)
        control_layout.addWidget(self.position_slider)

        # Etiqueta que muestra el tiempo actual y total del video
        self.time_label = QLabel("00:00 / 00:00")
        control_layout.addWidget(self.time_label)

        # Botones para retroceder y adelantar 5 segundos
        backward_button = QPushButton("<< 5s")
        backward_button.clicked.connect(lambda: self.video_player.skip(-5000))
        control_layout.addWidget(backward_button)

        forward_button = QPushButton("5s >>")
        forward_button.clicked.connect(lambda: self.video_player.skip(5000))
        control_layout.addWidget(forward_button)

        # Selector de velocidad de reproducción
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "1x", "1.5x", "2x", "4x"])
        self.speed_combo.setCurrentText("1x")
        self.speed_combo.currentTextChanged.connect(self.change_speed)
        control_layout.addWidget(self.speed_combo)

        parent_layout.addLayout(control_layout)

    def open_video(self):
        """Abre un diálogo para seleccionar un video y comienza su reproducción."""
        filePath, _ = QFileDialog.getOpenFileName(self, "Seleccionar Video", "", "Videos (*.mp4 *.avi *.mkv)")
        if filePath:
            self.video_player.load_video(filePath)
            self.video_player.play()
            self.play_pause_button.setText("Pausar")

    def toggle_play_pause(self):
        """
        Alterna entre reproducir y pausar el video.
        Al pausar, se captura el frame actual y se muestra el widget de anotación.
        Al reanudar, se oculta el overlay y se limpian las anotaciones previas.
        """
        if self.video_player.mediaPlayer.state() == self.video_player.mediaPlayer.PlayingState:
            self.video_player.pause()
            self.play_pause_button.setText("Reproducir")
            # Captura el frame actual mediante la pantalla (para widgets nativos)
            from PyQt5.QtWidgets import QApplication
            screen = QApplication.primaryScreen()
            snapshot = screen.grabWindow(self.video_player.video_widget.winId())
            self.annotation_widget.setBackground(snapshot)
            self.annotation_widget.setCursor(Qt.CrossCursor)
            self.annotation_widget.show()
            self.annotation_widget.raise_()  # Garantiza que el overlay quede al frente
        else:
            # Al reanudar, ocultamos el overlay y borramos las anotaciones previas
            self.annotation_widget.hide()
            self.annotation_widget.annotations.clear()
            self.video_player.play()
            self.play_pause_button.setText("Pausar")

    def update_position(self, position):
        """Actualiza el slider y la etiqueta de tiempo según la posición actual del video."""
        self.position_slider.setValue(position)
        current_time = QTime(0, 0, 0).addMSecs(position)
        total_time = QTime(0, 0, 0).addMSecs(self.total_duration)
        self.time_label.setText(f"{current_time.toString('mm:ss')} / {total_time.toString('mm:ss')}")

    def update_duration(self, duration):
        """Actualiza el rango del slider y la etiqueta de duración total del video."""
        self.position_slider.setRange(0, duration)
        self.total_duration = duration
        total_time = QTime(0, 0, 0).addMSecs(duration)
        self.time_label.setText(f"00:00 / {total_time.toString('mm:ss')}")

    def change_speed(self, text):
        """Cambia la velocidad de reproducción según el valor seleccionado."""
        speed = float(text.replace("x", ""))
        self.video_player.mediaPlayer.setPlaybackRate(speed)

    def keyPressEvent(self, event):
        """Permite controlar el video mediante las flechas y la barra espaciadora."""
        if event.key() == Qt.Key_Left:
            self.video_player.skip(-5000)
        elif event.key() == Qt.Key_Right:
            self.video_player.skip(5000)
        elif event.key() == Qt.Key_Space:
            self.toggle_play_pause()
        super().keyPressEvent(event)

    def process_annotation(self, especie, bounding_box):
        """Procesa cada anotación realizada (aquí se imprime la información en consola)."""
        print(f"Anotación recibida: {especie}, área: {bounding_box.getRect()}")

    def resizeEvent(self, event):
        """Ajusta el tamaño del overlay de anotación al cambiar el tamaño del video."""
        super().resizeEvent(event)
        self.annotation_widget.setGeometry(self.video_player.video_widget.rect())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
