from PyQt5.QtCore import QUrl, QObject, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class VideoPlayer(QObject):
    videoPaused = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 480)
        self.mediaPlayer.setVideoOutput(self.video_widget)

    def load_video(self, video_path):
        media = QMediaContent(QUrl.fromLocalFile(video_path))
        self.mediaPlayer.setMedia(media)
        print("Video cargado:", video_path)

    def play(self):
        self.mediaPlayer.play()
        print("Reproduciendo video...")

    def pause(self):
        self.mediaPlayer.pause()
        current_time = self.mediaPlayer.position() / 1000.0
        print("Video pausado en", current_time, "segundos")
        self.videoPaused.emit(current_time)

    def skip(self, ms):
        new_position = self.mediaPlayer.position() + ms
        self.mediaPlayer.setPosition(new_position)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
