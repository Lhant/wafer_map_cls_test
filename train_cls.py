from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolo11n-cls.pt")

    # Train the model
    results = model.train(data="wafer_map", epochs=100, imgsz=128)