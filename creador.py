import cv2

def main():

    video_path = 'data/sea.mp4'

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error al abrir el video")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Fin del video")

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()