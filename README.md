# textImage
## Getting Started
### Prerequisites
* create virtual environment
* install requirements
```
 pip install -r requirements.txt
```
### Create pretrained model from downloaded weights
Clone repo
```
git clone git@github.com:epsonik/textImage.git
```
Download the pre-trained YOLO v3 weights file from to the current directory in terminal using
```
wget https://pjreddie.com/media/files/yolov3.weights
```
Run
```
create_model.py
```
this will create file with pretrained model
```
model.h5
```
### Create report

Create report with original image, boxed image and certainty factors for recognized classes

login to the virtual environment:
```
conda activate <v_env_name>
```
Change path to the image in .jpg format in file main.py. File now must be from IMAGES
directory:
```
input_filename = 'bicycle/bicycle.jpg'
```
In example above image 'bicycle.jpg' is from subdirectory bicycle and has name bicycle.jpg.
Run creating report
```
python main.py
```
Report is created in project main directory, in the file 'report.xlsx'
### Report srtructure
Report is in .xlsx. Have 2 worksheets:
 images with boxed and original image
 data  with bounding boxes 
Each bounding box table have class name label in left upper corner.
 First column is the name of the position. Options:
left_orientation
right_orientation
top_orientation
bottom_orientation
Other columns are the name of the metod used for certainty factor. Now are implemented:
centroid method
area methos