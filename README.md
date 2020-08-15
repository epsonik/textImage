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
