"""Perform test request"""
import pprint
import argparse
import requests
import json
import os

DETECTION_URL = "http://localhost:5001/v1/risk_objects/"
TEST_IMAGE = "madrid_test_image.jpg"

def show_visualization(img, bounding_boxes, save=False, name=None):
    name = os.path.basename(name)
    from PIL import Image, ImageFont, ImageDraw
    if type(img) == bytes:  
        import io
        img = Image.open(io.BytesIO(image_data))
    elif type(img) == str:
        img = Image.open(img)
    width, height = img.size
    font = ImageFont.truetype("Gidole-Regular.ttf", size=int(height/40))
    for bounding_box in bounding_boxes:
        draw = ImageDraw.Draw(img)
        coords = ((bounding_box['xmin'], bounding_box['ymin']), (bounding_box['xmax'], bounding_box['ymax']))
        draw.rectangle(coords, outline ="yellow", width=5)
        label_text = bounding_box['name'] + ' conf:' + str(bounding_box['confidence'])
        label_box = draw.textsize(label_text, font)
        draw.rectangle(((coords[0][0], coords[0][1]),(coords[0][0] + label_box[0] +5, coords[0][1] + label_box[1] + 5)), outline="yellow", fill="yellow", width=10)
        draw.text(coords[0], label_text, (0,0,0), font=font)
    if save:
        if 'exif' in img.info.keys():
            img.save(f"./detections/bbxes_{name}", exif=img.info['exif'])
        else:
            img.save(f"./detections/bbxes_{name}")
    else:
        img.show()
    

parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str, default=TEST_IMAGE, help='Input image for detection')
parser.add_argument('--url', type=str, default=DETECTION_URL, help='Detection service URL and port as example.com:6001/v1/risk_objects/')
parser.add_argument('--show', action='store_true', help='Show visualization of results')
parser.add_argument('--save', action='store_true', help='Save results to a new file')
parser.add_argument('--jsonsave', action='store_true', help='Save results to JSON file')
opt = parser.parse_args()

image_data = open(opt.image, "rb").read()
response = requests.post(opt.url, files={"image": image_data}).json()
pprint.pprint(response)
if opt.show:
    show_visualization(image_data, response)
if opt.save:
    show_visualization(image_data, response, save=True, name=opt.image)
if opt.jsonsave:
    with open(f"{opt.image}.json", "w") as outfile:
        json.dump(response, outfile)
