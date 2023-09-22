"""Clean photos

This script checks if the scraped pictures are portrets and stores the results in a csv.

This script requires detectron2 and pandas to be installed within your Python
environment.

Usage:
------
python3 clean_photos.py input_csv output_csv
    input_csv
        path to a csv with at least the column filename
    output_csv
        path for the resulting csv
"""

import csv
from sys import argv

# import some common detectron2 utilities
import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import cv2
import pandas as pd



# workflow
# 1 de lijst met bestandsnamen (csv) wordt uitgelezen
# 2 op de foto wordt gekeken of er 1 of meer mensen op de foto staan
# 3 het resultaat komt in een csv

# detectron2 is nodig voor dit script. 
# installatie instructies hier: https://detectron2.readthedocs.io/en/latest/tutorials/install.html
cfg = get_cfg()
treshold = 0.7
# you need a list of the files, e.g. via Siegfried
files = argv[1]
csv_filename = argv[2]
filename_key = 'filename'

# lines bestaat uit: filename, aantal gezichten
lines = [["path", "aantal gezichten"]]


# setup detection model
def setup_detection_model(treshold): 
    print("setting up model")  
    cfg.MODEL.DEVICE = 'cpu'
    cfg.merge_from_file(model_zoo.get_config_file(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = treshold  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)
    print("done with setting up model")
    return predictor

# gegevens worden neergeschreven in een csv
def write_data(data):
    print("writing data")
    with open(csv_filename, "w") as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerows(data)
    output_csv.close()
   
# deze functie checkt of 
def is_portrait(predictor, photo):
    # noot aan mezelf: dit is eigenlijk een slechte functie. de return en set moeten gescheiden worden
    print("is {} a portrait?".format(photo))

    image = cv2.imread(photo)

    try:
        outputs = predictor(image)


    except:
        print(f"{photo} could not be read")
        portrait = False
        result = "image could not be read"
    
    else: 
        instances = outputs["instances"]
        count_instances = len(instances) 
        result = "portrait"
        portrait = True
        
        if  count_instances > 1:
            print("multiple instances found on " + str(photo))
            result = "group"
            portrait = False

        elif count_instances == 0:
            print("zero instances found on " + str(photo))
            result = "no person"
            portrait = False
        
        else:
            print("one instance found on " + str(photo))
    
    finally:
        lines.append([photo, result])
        return portrait

predictor = setup_detection_model(treshold)
list_photos = pd.read_csv(files)
for photo in list_photos[filename_key]:
    filename = photo
    if is_portrait(predictor, filename):
        print("{} is a portrait\n".format(filename))
    else:
        print("{} is not a portrait\n".format(filename))

write_data(lines)
