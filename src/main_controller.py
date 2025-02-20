import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QSlider, QAction, QFileDialog, QComboBox, QLabel)
from PyQt5.QtCore import Qt, QTime
from video_player import VideoPlayer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reproductor de Video")
        self.setGeometry(100, 100, 800, 600)
        self.create_menu()
        self.setFocusPolicy(Qt.StrongFocus)
        self.total_duration = 0

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Instanciar el VideoPlayer y agregar su widget
        self.video_player = VideoPlayer()
        layout.addWidget(self.video_player.video_widget)

        # Configurar controles de reproducción
        self.setup_controls(layout)

        # Conectar señales para actualizar el slider y el tiempo
        self.video_player.mediaPlayer.positionChanged.connect(self.update_position)
        self.video_player.mediaPlayer.durationChanged.connect(self.update_duration)

        # Inicializar tiempo total en 0
        self.total_duration = 0

    def create_menu(self):
        # Crear un menú File para abrir videos
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        open_action = QAction("Abrir video", self)
        open_action.triggered.connect(self.open_video)
        file_menu.addAction(open_action)

    def setup_controls(self, parent_layout):
        """Configura y agrega los controles de reproducción a la interfaz."""
        control_layout = QHBoxLayout()

        # Botón Play/Pausa
        self.play_pause_button = QPushButton("Pausar")
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        control_layout.addWidget(self.play_pause_button)

        # Slider de posición
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.video_player.set_position)
        control_layout.addWidget(self.position_slider)

        # **Etiqueta para mostrar el tiempo de reproducción**
        self.time_label = QLabel("00:00 / 00:00")
        control_layout.addWidget(self.time_label)

        # Botón para retroceder 5 segundos
        backward_button = QPushButton("<< 5s")
        backward_button.clicked.connect(lambda: self.video_player.skip(-5000))
        control_layout.addWidget(backward_button)

        # Botón para adelantar 5 segundos
        forward_button = QPushButton("5s >>")
        forward_button.clicked.connect(lambda: self.video_player.skip(5000))
        control_layout.addWidget(forward_button)

        # Combo para cambiar velocidad de reproducción
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "1x", "1.5x", "2x", "4x", "8x"])
        self.speed_combo.setCurrentText("1x")
        self.speed_combo.currentTextChanged.connect(self.change_speed)
        control_layout.addWidget(self.speed_combo)

        # Agregar los controles al layout principal
        parent_layout.addLayout(control_layout)

    def open_video(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Seleccionar Video", "", "Videos (*.mp4 *.avi *.mkv)")
        if filePath:
            self.video_player.load_video(filePath)
            self.video_player.play()
            self.play_pause_button.setText("Pausar")

    def toggle_play_pause(self):
        if self.video_player.mediaPlayer.state() == self.video_player.mediaPlayer.PlayingState:
            self.video_player.pause()
            self.play_pause_button.setText("Reproducir")
        else:
            self.video_player.play()
            self.play_pause_button.setText("Pausar")

    def update_position(self, position):
        """Actualizar el slider y el tiempo de reproducción."""
        self.position_slider.setValue(position)

        # Convertir tiempo actual a minutos y segundos
        current_time = QTime(0, 0, 0).addMSecs(position)
        total_time = QTime(0, 0, 0).addMSecs(self.total_duration)

        # Formato MM:SS / MM:SS
        self.time_label.setText(f"{current_time.toString('mm:ss')} / {total_time.toString('mm:ss')}")

    def update_duration(self, duration):
        """Actualizar la duración total del video."""
        self.position_slider.setRange(0, duration)
        self.total_duration = duration  # Guardar duración total

        # Actualizar la etiqueta del tiempo total
        total_time = QTime(0, 0, 0).addMSecs(duration)
        self.time_label.setText(f"00:00 / {total_time.toString('mm:ss')}")

    def change_speed(self, text):
        speed = float(text.replace("x", ""))
        self.video_player.mediaPlayer.setPlaybackRate(speed)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.video_player.skip(-5000)
        elif event.key() == Qt.Key_Right:
            self.video_player.skip(5000)
        elif event.key() == Qt.Key_Space:
            self.toggle_play_pause()
        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
