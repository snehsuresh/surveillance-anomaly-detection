import cv2
import numpy as np
from PIL import Image
from inference_sdk import InferenceHTTPClient
from expressiondetection.config.model_config import API_URL, API_KEY, MODEL_ID
from expressiondetection.utils.main_utils import translate_label

# Initialize the RoboFlow client
CLIENT = InferenceHTTPClient(api_url=API_URL, api_key=API_KEY)


def yolo_detect(frame):
    try:
        # Resize the image to 416x416 pixels
        resized_frame = cv2.resize(frame, (416, 416))

        # Convert resized image to RGB
        img_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

        # Send the image to RoboFlow API for inference
        result = CLIENT.infer(img_rgb, model_id=MODEL_ID)
        print(result)  # For debugging

        # Process the result to get detection labels
        predictions = result.get("predictions", {})
        if predictions:
            # Find the class with the highest confidence
            detected_class = max(predictions.items(), key=lambda x: x[1]["confidence"])
            label = detected_class[0]  # Class name
            # confidence = detected_class[1]["confidence"]
            return translate_label(label)
            # Return label or "Processing.." based on confidence
            # if confidence >= 0.4:
            #     return translate_label(label)
            # else:
            #     return "Processing.."
        else:
            return "No predictions found"
    except Exception as e:
        print(f"Error in yolo_detect: {e}")
        return None
