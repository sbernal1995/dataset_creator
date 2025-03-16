import os

class DataManager:
    def __init__(self, output_folder="output"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        self.last_file = None

    def save_frame_and_data(self, video_name, especie, timestamp, bounding_box, frame_pixmap):
        print(f"  Video name: {video_name}")
        print(f"  Especie: {especie}")
        print(f"  Timestamp: {timestamp}")
        print(f"  Bounding Box (rect): {bounding_box.getRect()}")
        print(f"  Frame pixmap: {frame_pixmap}")

        file_timestamp = timestamp.replace(":", "_")
        base_png_filename = f"{video_name}_{especie}_{file_timestamp}.png"
        png_filename = base_png_filename

        image_path = os.path.join(self.output_folder, png_filename)
        suffix = 1
        # Se incrementa en 1 un sufijo para cuando es la misma especie en el mismo timing
        while os.path.exists(image_path):
            png_filename = f"{video_name}_{especie}_{file_timestamp}{suffix}.png"
            image_path = os.path.join(self.output_folder, png_filename)
            suffix += 1

        # Aca extraemos coordenadas del bounding_box (x, y, width, height)
        x, y, width, height = bounding_box.getRect()
        x1 = x
        y1 = y
        x2 = x + width
        y2 = y + height

        if frame_pixmap.save(image_path):
            print(f"Imagen guardada en {image_path}")
        else:
            print("Error al guardar la imagen.")

        # Usamos este formato: "<png_filename> <NombreDeEspecie> <X1> <X2> <Y1> <Y2>"
        txt_entry = f"{png_filename} {especie} {x1} {x2} {y1} {y2}\n"
        txt_filename = f"{video_name}.txt"
        txt_path = os.path.join(self.output_folder, txt_filename)

        if os.path.exists(txt_path):
            print(f"El archivo {txt_filename} ya existe. Se agregará la nueva entrada.")
            with open(txt_path, "a") as f:
                f.write(txt_entry)
        else:
            print(f"El archivo {txt_filename} no existe. Se creará uno nuevo.")
            with open(txt_path, "w") as f:
                f.write(txt_entry)

        print("Entrada guardada en el archivo TXT:")
        print(txt_entry)
