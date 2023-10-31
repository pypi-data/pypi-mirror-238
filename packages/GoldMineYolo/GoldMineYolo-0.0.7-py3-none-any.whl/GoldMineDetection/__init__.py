from ultralytics import YOLO
def detect_mine(imagePath):
    #
    model = YOLO('currentModel.pt')  # takes current model
    print("detecting a mine!")
    print(imagePath)
    return model.predict(source=imagePath, save=True, conf=.45)

