# data_manager.py
import os


class DataManager:
    def __init__(self, output_folder="output"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        self.last_file = None

    def save_frame_and_data(self, video_name, especie, timestamp, bounding_box, frame_pixmap):
        # Genera nombres de archivo de ejemplo y guarda datos en consola
        time_str = f"{timestamp:.2f}"
        base_filename = f"{video_name}_{especie}_{time_str}"
        image_path = os.path.join(self.output_folder, base_filename + ".png")
        txt_path = os.path.join(self.output_folder, base_filename + ".txt")

        # Supongamos que guardamos la imagen (frame_pixmap.save(image_path)) y los datos en el txt
        print(f"Guardando imagen en {image_path}")
        print(f"Guardando datos en {txt_path}")
        # Aquí iría el código real de guardado
        self.last_file = (image_path, txt_path)
