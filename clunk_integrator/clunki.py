import time
import pprint
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from webdav3.client import Client
from PIL import Image, ImageFont, ImageDraw

class Clunki():
    def __init__(self, **kwargs):
        _service_host = "fasolt4.willab.fi"
        self._detection_service_url = "http://"+_service_host+":5001/v1/risk_objects/"
        self._file_storage_url = "https://"+_service_host+":8883/dav/"
        self.dav_options = {
            'webdav_hostname': self._file_storage_url,
            'webdav_login':    "bimuser",
            'webdav_password': "bimproveK0ukku55",
            'disable_check': True
        }
        self.os_incoming_path = '/var/cells/data/bimprove/incoming'
        self.webdav_incoming_path = 'bimprove-image-storage/incoming'
        self.webdav_processed_path = 'bimprove-image-storage/processed'

    def insert_to_risk_db(self, detections, orig_file_url, bb_file_url):
        pass

    def add_bounding_box_to_img(self, os_file_path, detections):
        img = Image.open(os_file_path)
        file_name = os_file_path.strip(self.os_incoming_path+'/')
        path_name = os_file_path.strip(file_name)
        width, height = img.size
        font = ImageFont.truetype("Gidole-Regular.ttf", size=int(height/40))
        for detection in detections:
            draw = ImageDraw.Draw(img)
            coords = ((detection['xmin'], detection['ymin']), (detection['xmax'], detection['ymax']))
            draw.rectangle(coords, outline ="yellow", width=30)
            label_text = detection['name'] + ' conf:' + str(detection['confidence'])
            label_box = draw.textsize(label_text, font)
            draw.rectangle(((coords[0][0], coords[0][1]),(coords[0][0] + label_box[0] +5, coords[0][1] + label_box[1] + 5)), outline="yellow", fill="yellow", width=10)
            draw.text(coords[0], label_text, (0,0,0), font=font)
        if len(detections) > 0:
           new_file_name = path_name + "bbxes_"+file_name
           img.save(new_file_name, "JPEG")
           return new_file_name
        return None

    def move_files(self, os_file_path):
        #Extract file name from the OS file path
        file_name = os_file_path.strip(self.os_incoming_path+'/')
        if len(file_name) > 0:
            client=Client(self.dav_options)
            client.verify=False
            print(self.dav_options)
            print(client.list())
            if file_name in client.list(self.webdav_incoming_path):
                client.move(remote_path_from=self.webdav_incoming_path+'/'+file_name, remote_path_to=self.webdav_processed_path+'/'+file_name)

    def do_inference(self, file_path):
        image_data = open(file_path, "rb").read()
        response = requests.post(self._detection_service_url, files={"image": image_data})
        if len(response.json()) > 0:
            new_f = self.add_bounding_box_to_img(file_path, response.json)
            pprint.pprint(response.json())
            print(new_f)
            #self.move_files(file_path)

    def on_created(self, event): # when file is created
        print("Got event for file %s" %event.src_path)
        img_ext_list = ['jpg', 'gif', 'tif', 'png']
        img_ext = event.src_path.split('.')[-1]
        if img_ext.lower() in img_ext_list:
            self.do_inference(event.src_path)

    def start_file_observer(self):
        self.observer = Observer()
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_created = self.on_created
        self.observer.schedule(self.event_handler, path=self.os_incoming_path)
        self.observer.start()

if __name__ == "__main__":
    clunk = Clunki()
    clunk.start_file_observer()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        clunk.observer.stop()
    clunk.observer.join()
