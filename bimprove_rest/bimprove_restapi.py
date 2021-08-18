"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io

import torch
from PIL import Image
from flask import Flask, request, render_template, url_for, send_file, abort
import os

#app = Flask(__name__, static_folder='/static', static_url_path='/static')
app = Flask(__name__)

DETECTION_URL = "/v1/risk_objects/"

@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
        return
    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))  
        results = model(img, size=640)  # reduce size=320 for faster inference
        return results.pandas().xyxy[0].to_json(orient="records")

@app.route(DETECTION_URL, methods=["GET"])
def give_documentation():
    return render_template('bimprove_not_here.html', full_url=url_for('predict', _external=True))

@app.route('/static/<imgname>', methods=['GET'])
def give_static_file(imgname):
    try:
        return send_file(f'static/{imgname}')
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5001, type=int, help="port number")
    args = parser.parse_args()

    #model = torch.hub.load('path/to/yolov5', 'custom', path='path/to/best.pt', source='local')
    #model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=True)  # force_reload to recache
    #model = torch.load("best.pt")
    #model = torch.hub.load("ultralytics/yolov5", 'custom', path='./yolov5m.pt').to('cpu')
    model = torch.hub.load("ultralytics/yolov5", 'custom', path='./best.pt').to('cpu')

    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
