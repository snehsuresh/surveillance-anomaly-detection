from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com", api_key="ZqSDWrJegOAv65BhaCvQ"
)

result = CLIENT.infer(
    "/Users/snehsuresh/Downloads/Expression.v3i.multiclass/train/bs001_E_HAPPY_0_png_jpg.rf.9085c07e1dcf63e5de8bf8a16d29e00e.jpg",
    model_id="expression-bivfq/1",
)

print(result)
