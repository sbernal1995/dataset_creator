import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton

from video_player import VideoPlayer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reproductor de Video")
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Instanciar y agregar el widget de video
        self.video_player = VideoPlayer()
        layout.addWidget(self.video_player.video_widget)

        # Botón para pausar (por ejemplo)
        pause_button = QPushButton("Pausar Video")
        pause_button.clicked.connect(self.video_player.pause)
        layout.addWidget(pause_button)

        self.setCentralWidget(central_widget)

        # Cargar y reproducir el video
        self.video_player.load_video("data/sea.mp4")
        self.video_player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
