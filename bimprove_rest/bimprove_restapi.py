"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
import torch
from PIL import Image
from flask import Flask, Response, request, render_template, url_for, send_file, abort
import os
import time

img_size = 960
model_file_name = './all_combined.e200.is960.freeze.adamw.autobatch.ft.pt'

app = Flask(__name__)

DETECTION_URL = "/v1/risk_objects/"
PYDIO_INCOMING_DIR = '/var/cells/data/bimprove/incoming'
SUPPORTED_FILE_EXTS = ['jpg', 'gif', 'tif', 'png', 'jpeg']

@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
        return
    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        if request.args and 'store' in request.args.keys() and request.args['store'] == 'True':
            if 'origfname' in request.args.keys():
                origfname = request.args['origfname']
            else:
                origfname = 'unnamed_image_' + str(int(time.time())) + '.jpg'
            if not os.path.isdir(PYDIO_INCOMING_DIR):
                return Response('Path /var/cells/data/bimprove/incoming does not exist', status=500)
            if origfname.split('.')[-1] not in SUPPORTED_FILE_EXTS:
                print("Crash here", image_file.filename)
                return Response(f'The only supported image formats are {SUPPORTED_FILE_EXTS}', status=400)
            #Save image to '/var/cells/data/bimprove/incoming'
            if 'exif' in img.info.keys():
                img.save(f"/var/cells/data/bimprove/incoming/{origfname}", exif=img.info['exif'])
            else:
                img.save(f"/var/cells/data/bimprove/incoming/{origfname}")
            return Response(f'{origfname} file moved to processing queue, wait for a moment for the results to appear', status=200)                   
        else:
            results = model(img, size=img_size)  # reduce size=320 for faster inference
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

    #Use GPU if available on your environment
    #model = torch.hub.load("ultralytics/yolov5", 'custom', path=model_file_name).to('gpu')
    model = torch.hub.load("ultralytics/yolov5", 'custom', path=model_file_name).to('cpu')
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
