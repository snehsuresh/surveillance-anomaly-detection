import cv2
import numpy as np
import time
from PIL import Image
from inference_sdk import InferenceHTTPClient

# Initialize the RoboFlow client
CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com", api_key="ZqSDWrJegOAv65BhaCvQ"
)

# Dictionary for translating Indonesian labels to English
label_translation = {
    "Jijik": "Disgusted",
    "Kaget": "Surprised",
    "Marah": "Angry",
    "Sedih": "Sad",
    "Senang": "Happy",
    "Takut": "Fearful",
    "Tidak Berekspresi": "No Expression",
}


def translate_label(indonesian_label):
    return label_translation.get(indonesian_label, "Unknown Label")


def yolo_detect(frame):
    try:

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil.show()
        # Send the image to RoboFlow API for inference
        result = CLIENT.infer(img_rgb, model_id="expression-bivfq/1")
        print(result)  # For debugging

        # Process the result to get detection labels
        predictions = result.get("predictions", {})
        if predictions:
            # Find the class with the highest confidence
            detected_class = max(predictions.items(), key=lambda x: x[1]["confidence"])
            label = detected_class[0]  # Class name
            return translate_label(label)
        else:
            return "No predictions found"
    except Exception as e:
        print(f"Error in yolo_detect: {e}")
        return None


def test_yolo(image_path):
    img = cv2.imread(image_path)

    detected_label = yolo_detect(img)
    print(f"Detected label: {detected_label}")

    # Display the image
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_pil.show()


def predictLive():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    last_detection_time = time.time()
    detection_interval = 5
    last_detection_label = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Detect faces in color image
            faces = face_cascade.detectMultiScale(
                frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            current_time = time.time()
            if current_time - last_detection_time > detection_interval:
                for x, y, w, h in faces:
                    face_region = frame[y : y + h, x : x + w]
                    detected_label = yolo_detect(face_region)
                    if detected_label:
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


if __name__ == "__main__":
    predictLive()
    # test_yolo(
    #     "/Users/snehsuresh/Downloads/Expression.v3i.multiclass/train/bs001_E_HAPPY_0_png_jpg.rf.9085c07e1dcf63e5de8bf8a16d29e00e.jpg"
    # )
