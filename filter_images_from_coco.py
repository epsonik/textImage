import os

import requests
from pycocotools.coco import COCO

# Download images from 5 categories
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# path to the directory with images from coco dataset
TRAIN_IMAGES_DIRECTORY = "/Users/mateuszb/cocoapi/coco/images/val2014"
# path to the file with annotations.json
TRAIN_ANNOTATIONS_PATH = "/Users/mateuszb/cocoapi/coco/annotations/instances_train2014.json"

coco = COCO(TRAIN_ANNOTATIONS_PATH)
# Specify a list of category names of interest
cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))


def download_images_from_coco(categoryNames):
    for categoryName in categoryNames:
        catIds = coco.getCatIds(catNms=[categoryName])
        # Get the corresponding image ids and images using loadImgs
        imgIds = coco.getImgIds(catIds=catIds)
        images = coco.loadImgs(imgIds)
        try:
            # Create target Directory
            os.mkdir("IMAGES/" + categoryName)
            print("Directory ", categoryName, " Created ")
            for im in images[:10]:
                img_data = requests.get(im['coco_url']).content
                print('test')
                with open(os.path.join(THIS_FOLDER, "IMAGES/" + categoryName + "/" + im['file_name']), 'wb') as handler:
                    handler.write(img_data)
        except FileExistsError:
            print("Directory ", categoryName, " already exists")


download_images_from_coco(['car', 'dog', 'elephant', 'giraffe', 'bicycle'])
