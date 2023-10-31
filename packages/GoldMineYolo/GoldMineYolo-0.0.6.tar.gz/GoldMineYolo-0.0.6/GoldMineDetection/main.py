import os
import ultralytics
import yaml
from ultralytics import YOLO
from IPython import display
from importlib import resources
import io
HOME = os.getcwd()
print(HOME)

display.clear_output()

ultralytics.checks()
from IPython.display import display, Image
from dotenv import load_dotenv
load_dotenv()
from roboflow import Roboflow
#with open('../creds.yaml', 'r') as file:
 #   prime_service = yaml.safe_load(file)
# create a .env file to run from
api_key = os.getenv("ROBOFLOW_API_KEY")
# finds the roboflow dataset online and downloads the selected version of the set


rf = Roboflow(api_key=api_key)
#rf = Roboflow(api_key=prime_service['creds'])
project = rf.workspace("enviromental-robotics").project("gold-mine-detection")
if not os.path.isdir("Gold-Mine-Detection-8"):
    dataset = project.version(8).download("yolov8")
else:
    dataset = project.version(8)
    
    
print(dataset)
# finds the information pertneatn to the dataset

# loc = dataset.location + '\data.yaml'

# with resources.open_binary('src',dataset.location + '\data.yaml') as fp:
#     loc=fp.read()


# creates a model based on the selected weights
model = YOLO('currentModel.pt')  # takes current model

# uncomment to train another version, you must update the current model if you do
# model.train(data=loc, epochs=13, imgsz=640, plots=True)

print("trained!")
# creates states of the model
#metrics = model.val(data=loc, save=False)

# metrics.box.map    # map50-95
# metrics.box.map50  # map50
# metrics.box.map75  # map75
# metrics.box.maps   # a list contains map50-95 of each category

print("printed metrics:")
#print(metrics)
#pics = ['testPic2.jpg', 'testPicture.jpg']

# model.predict(source='..\drone Photos jpg', save=True, conf=.45)
print("predicted")


# project.version(6).deploy(model_type="yolov8", model_path="runs/detect/train/")
# project.version(DATASET_VERSION).deploy(model_type=”yolov8”, model_path=f”{HOME}/runs/detect/train/”)
from GoldMineDetection import  detect_mine
detect_mine("testPic.jpg")

class image_processor:
    def __init__(self, filePath):

        
        print(" init")
        self.filePath=filePath
        self.findMine()

    def findMine(self):
        temp =model.predict(source=self.filePath, save=False, conf=.45)
        return temp

# im = image_processor("testPic.jpg")
# print("atrubut")


#print(one_image('..\..\drone Photos jpg\DJI_0216.jpg'))