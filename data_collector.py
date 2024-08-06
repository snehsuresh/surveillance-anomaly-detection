import os
import cv2
import time
import uuid

IMAGE_PATH = "CollectedImages"

labels = ["Robbery", "Fight", "Murder", "Harrassment"]

number_of_images = 50

for label in labels:
    img_path = os.path.join(IMAGE_PATH, label)
    os.mkdirs(img_path)

    cap = cv2.VideoCapture(0)
    print(f"Collecting images for {label}")
    time.sleep(5)

    for imgnum in range(number_of_images):
        ret, frame = cap.read()
        imagename = os.path.join(
            IMAGE_PATH, label, label + "." + "{}.jpg".format(str(uuid.uuid1()))
        )
        cv2.imwrite(imagename, frame)
        cv2.imshow("frame", frame)
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()