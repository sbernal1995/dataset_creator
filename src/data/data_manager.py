# data_manager.py
import os


class DataManager:
    def __init__(self, output_folder="output"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        self.last_file = None

    def save_frame_and_data(self, video_name, especie, timestamp, bounding_box, frame_pixmap):
        print("Guardando datos...")
        print(f"  Video name: {video_name}")
        print(f"  Especie: {especie}")
        print(f"  Timestamp: {timestamp}")
        print(f"  Bounding Box (rect): {bounding_box.getRect()}")
        print(f"  Frame pixmap: {frame_pixmap}")


