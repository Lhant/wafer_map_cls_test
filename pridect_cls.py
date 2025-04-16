from ultralytics import YOLO

# Load a model
# model = YOLO("yolo11n-cls.pt")  # load an official model
model = YOLO("runs/classify/train/weights/best.pt")  # load a custom model
model.to('cpu')
# Predict with the model
results = model("img/img_7.png",device='cpu')  # predict on an image

# Access the top class index and confidence
top_class_index = results[0].probs.top1  # Get the index of the top class
top_class_name = model.names[top_class_index]  # Get the class name from the model
top_class_prob = results[0].probs.top1conf  # Get the confidence of the top class

print(f"类别名称: {top_class_name}, 概率: {top_class_prob:.2f}")