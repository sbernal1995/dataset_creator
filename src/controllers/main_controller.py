# src/controllers/main_controller.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QSlider, QAction, QFileDialog,
                             QComboBox, QLabel, QStackedLayout)
from PyQt5.QtCore import Qt, QTime, QSize

from src.data.data_manager import DataManager
from src.widgets.annotation import AnnotationWidget
from src.widgets.video_player import VideoPlayer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._saved_size = None
        self.setWindowTitle("Reproductor de Video")
        self.setGeometry(100, 100, 800, 600)
        self.create_menu()
        self.setFocusPolicy(Qt.StrongFocus)
        self.total_duration = 0

        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Contenedor para video y anotación usando QStackedLayout
        video_container = QWidget()
        self.stack_layout = QStackedLayout(video_container)
        self.stack_layout.setStackingMode(QStackedLayout.StackAll)

        # Instanciar el VideoPlayer y ajustar su widget
        self.video_player = VideoPlayer()
        self.video_player.video_widget.setAttribute(Qt.WA_NativeWindow, False)
        self.stack_layout.addWidget(self.video_player.video_widget)

        # Instanciar el AnnotationWidget y agregarlo al stack
        self.annotation_widget = AnnotationWidget(video_container)
        self.annotation_widget.setGeometry(self.video_player.video_widget.rect())
        self.annotation_widget.hide()  # Inicia oculto
        self.annotation_widget.annotationCompleted.connect(self.process_annotation)
        self.stack_layout.addWidget(self.annotation_widget)

        #Instanciar el DataManager
        self.data_manager = DataManager()

        # Agregar el contenedor del video (con ambos widgets) al layout principal
        main_layout.addWidget(video_container)

        # Agregar controles de reproducción debajo del video
        self.setup_controls(main_layout)

        # Conectar señales del reproductor
        self.video_player.mediaPlayer.positionChanged.connect(self.update_position)
        self.video_player.mediaPlayer.durationChanged.connect(self.update_duration)

    def create_menu(self):
        """Crea el menú de la aplicación con opciones para abrir video y ver ayuda."""
        menu = self.menuBar()
        file_menu = menu.addMenu("Archivo")
        open_action = QAction("Abrir video", self)
        open_action.triggered.connect(self.open_video)
        file_menu.addAction(open_action)

        # Agregar menú de Help
        help_menu = menu.addMenu("Ayuda")
        help_action = QAction("Instrucciones", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def show_help(self):
        """Muestra el diálogo de ayuda con instrucciones."""
        from src.dialogs.help_dialog import HelpDialog
        dialog = HelpDialog(self)
        dialog.exec_()

    def setup_controls(self, parent_layout):
        control_layout = QHBoxLayout()

        self.play_pause_button = QPushButton("Pausar")
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        control_layout.addWidget(self.play_pause_button)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.video_player.set_position)
        control_layout.addWidget(self.position_slider)

        self.time_label = QLabel("00:00 / 00:00")
        control_layout.addWidget(self.time_label)

        backward_button = QPushButton("<< 5s")
        backward_button.clicked.connect(lambda: self.video_player.skip(-5000))
        control_layout.addWidget(backward_button)

        forward_button = QPushButton("5s >>")
        forward_button.clicked.connect(lambda: self.video_player.skip(5000))
        control_layout.addWidget(forward_button)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "1x", "1.5x", "2x", "4x"])
        self.speed_combo.setCurrentText("1x")
        self.speed_combo.currentTextChanged.connect(self.change_speed)
        control_layout.addWidget(self.speed_combo)

        parent_layout.addLayout(control_layout)

    def open_video(self):
        """Abre un diálogo para seleccionar un video y comienza su reproducción."""
        import os
        initial_dir = ""
        if hasattr(self, "last_video") and self.last_video:
            initial_dir = os.path.dirname(self.last_video)
        filePath, _ = QFileDialog.getOpenFileName(self, "Seleccionar Video", initial_dir, "Videos (*.mp4 *.avi *.mkv)")
        if filePath:
            self.last_video = filePath
            self.video_player.load_video(filePath)
            self.video_player.play()
            self.play_pause_button.setText("Pausar")

    def toggle_play_pause(self):
        if self.video_player.mediaPlayer.state() == self.video_player.mediaPlayer.PlayingState:
            self.video_player.pause()
            self._saved_size = self.size()
            self.setFixedSize(self._saved_size)
            self.play_pause_button.setText("Reproducir")
            from PyQt5.QtWidgets import QApplication
            screen = QApplication.primaryScreen()
            snapshot = screen.grabWindow(self.video_player.video_widget.winId())
            self.annotation_widget.setBackground(snapshot)
            self.annotation_widget.setCursor(Qt.CrossCursor)
            self.annotation_widget.show()
            self.annotation_widget.raise_()
        else:
            self.annotation_widget.hide()
            self.annotation_widget.annotations.clear()
            self.video_player.play()
            self.play_pause_button.setText("Pausar")
            self.setMinimumSize(0, 0)
            self.setMaximumSize(16777215, 16777215)


    def update_position(self, position):
        self.position_slider.setValue(position)
        current_time = QTime(0, 0, 0).addMSecs(position)
        total_time = QTime(0, 0, 0).addMSecs(self.total_duration)
        self.time_label.setText(f"{current_time.toString('mm:ss')} / {total_time.toString('mm:ss')}")

    def update_duration(self, duration):
        self.position_slider.setRange(0, duration)
        self.total_duration = duration
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

    def process_annotation(self, especie, bounding_box):
        print(f"Anotación recibida: {especie}, área: {bounding_box.getRect()}")

        import os
        # Obtener el nombre del video
        video_name = os.path.basename(self.last_video) if hasattr(self, "last_video") else "video_desconocido"

        # Formatear el timestamp en "mm:ss"
        from PyQt5.QtCore import QTime
        current_seconds = self.video_player.mediaPlayer.position() // 1000
        t = QTime(0, 0, 0).addSecs(current_seconds)
        formatted_timestamp = t.toString("mm:ss")

        # Capturar el frame actual del video
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        frame_pixmap = screen.grabWindow(self.video_player.video_widget.winId())

        # Mostrar en consola todos los datos que se enviarán al DataManager
        print("Datos enviados al DataManager:")
        print(f"  Video name: {video_name}")
        print(f"  Especie: {especie}")
        print(f"  Timestamp: {formatted_timestamp}")
        print(f"  Bounding Box (rect): {bounding_box.getRect()}")
        print(f"  Frame pixmap: {frame_pixmap}")

        # Llamar al DataManager con los datos
        self.data_manager.save_frame_and_data(video_name, especie, formatted_timestamp, bounding_box, frame_pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.annotation_widget.setGeometry(self.video_player.video_widget.rect())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
