import cv2
import time
from expressiondetection.yolo import yolo_detect
from expressiondetection.config.model_config import DETECTION_INTERVAL
from expressiondetection.utils.main_utils import speak_text


def predict_live():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    last_detection_time = time.time()
    last_detection_label = None
    last_audio_time = time.time() - 10  # Initial value to ensure first audio is played

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            faces = face_cascade.detectMultiScale(
                frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            current_time = time.time()

            if current_time - last_detection_time > DETECTION_INTERVAL:
                for x, y, w, h in faces:
                    face_region = frame[y : y + h, x : x + w]
                    detected_label = yolo_detect(face_region)

                    if detected_label:
                        # Check if the label has changed and if 10 seconds have passed
                        if detected_label != last_detection_label and (
                            current_time - last_audio_time > 10
                        ):
                            speak_text(f"The person is {detected_label}")
                            last_audio_time = (
                                current_time  # Update last audio playback time
                            )

                        last_detection_label = detected_label

                last_detection_time = current_time

            if last_detection_label:
                for x, y, w, h in faces:
                    cv2.putText(
                        frame,
                        last_detection_label,
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 0),
                        2,
                    )

            cv2.imshow("Real-Time Face Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera stopped!")
