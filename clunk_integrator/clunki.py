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
        self.os_processed_path = '/var/cells/data/bimprove/processed'
        self.os_temp_file_path = '/tmp'
        self.webdav_incoming_path = 'bimprove-image-storage/incoming'
        self.webdav_processed_path = 'bimprove-image-storage/processed'
        self.webdav_temp_path = 'bimprove-image-storage/temp'

    def insert_to_risk_db(self, file, fule):
        pass

    def add_bounding_box_to_img(self, os_file_path, detections):
        img = Image.open(os_file_path)
        base_file_name = os_file_path.replace(self.os_incoming_path+'/', '')
        width, height = img.size
        font = ImageFont.truetype("Gidole-Regular.ttf", size=int(height/40))
        if len(detections) > 0:
            for detection in detections:
                draw = ImageDraw.Draw(img)
                coords = ((detection['xmin'], detection['ymin']), (detection['xmax'], detection['ymax']))
                draw.rectangle(coords, outline ="yellow", width=30)
                label_text = detection['name'] + ' conf:' + str(detection['confidence'])
                label_box = draw.textsize(label_text, font)
                draw.rectangle(((coords[0][0], coords[0][1]),(coords[0][0] + label_box[0] +5, coords[0][1] + label_box[1] + 5)), outline="yellow", fill="yellow", width=10)
                draw.text(coords[0], label_text, (0,0,0), font=font)
            new_full_file_name = self.os_temp_file_path + '/bbxes_' + base_file_name
            img.save(new_full_file_name, "JPEG")
            return new_full_file_name
        return None

    def move_files(self, file_os_path, new_file_os_path):
        #Extract file name from the OS file path
        file_name = file_os_path.replace(self.os_incoming_path+'/', '')
        new_file_name = new_file_os_path.replace(self.os_temp_file_path+'/', '')
        if len(file_name) > 0 and len(new_file_name) > 0:
            client=Client(self.dav_options)
            client.verify=False
            if file_name in client.list(self.webdav_incoming_path):
                #Just copy the file, i.e. let pydio manage duplicate files and their naming..BWAHAH
                client.copy(remote_path_from=self.webdav_incoming_path+'/'+file_name, remote_path_to=self.webdav_processed_path+'/'+file_name)
                #'Uploade' file from local temp to webdav temp - uploading there manages sharing and caring automatically
            client.upload_sync(local_path=new_file_os_path, remote_path=self.webdav_temp_path+'/'+new_file_name)
            #Move file from webdav temp to processed folder shared
            if new_file_name in client.list(self.webdav_temp_path):
                #client.move(remote_path_from=self.webdav_temp_path+'/'+new_file_name, remote_path_to=self.webdav_processed_path+'/'+new_file_name)
                client.move(remote_path_from=self.webdav_temp_path+'/'+new_file_name, remote_path_to=self.webdav_processed_path+'/'+new_file_name)

    def do_inference(self, file_path):
        image_data = open(file_path, "rb").read()
        response = requests.post(self._detection_service_url, files={"image": image_data})
        if len(response.json()) > 0:
            new_temp_file_and_path = self.add_bounding_box_to_img(file_path, response.json())
            pprint.pprint(response.json())
            self.move_files(file_path, new_temp_file_and_path)

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
