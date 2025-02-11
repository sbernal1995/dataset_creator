from PyQt5.QtCore import QUrl, QObject, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoPlayer(QObject):
    videoPaused = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 480)
        self.player.setVideoOutput(self.video_widget)

    def load_video(self, video_path):
        media = QMediaContent(QUrl.fromLocalFile(video_path))
        self.player.setMedia(media)
        print("Video cargado:", video_path)

    def play(self):
        self.player.play()
        print("Reproduciendo video...")

    def pause(self):
        self.player.pause()
        current_time = self.player.position() / 1000.0
        print("Video pausado en", current_time, "segundos")
        self.videoPaused.emit(current_time)
