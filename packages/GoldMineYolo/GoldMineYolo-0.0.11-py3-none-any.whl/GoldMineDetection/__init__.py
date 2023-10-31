
def detect_mine(imagePath):
    from ultralytics import YOLO
    model = YOLO('currentModel.pt')  # takes current model
    print("detecting a mine!")
    print(imagePath)
    return model.predict(source=imagePath, save=True, conf=.45)

