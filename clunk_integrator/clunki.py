import time
import pprint
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from webdav3.client import Client

class Clunki():
    def __init__(self, **kwargs):
        _service_host = "fasolt4.willab.fi"
        self._detection_service_url = "http://"+_service_host+":5001/v1/risk_objects/"
        self._file_storage_url = "https://"+_service_host+":8883/dav"
        self.dav_options = {
            'webdav_hostname': self._file_storage_url,
            'webdav_login':    "admin",
            'webdav_password': "429Memfw",
            'disable_check': True
        }

    def insert_to_risk_db(self, detections, orig_file_url, bb_file_url):
        pass
    
    def move_files(self, file_path):
        client=Client(self.dav_options)
        client.verify=False
        client.move(remote_path_from="/personal-files/bouty.jpg", remote_path_to="/personal-files/test/bouty.jpg")
        pass
    
    def do_inference(self, file_path):
        image_data = open(event.src_path, "rb").read()
        response = requests.post(self._detection_service_url, files={"image": image_data}).json()
        pprint.pprint(response)        

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
        self.observer.schedule(self.event_handler, path='/var/cells/data/bimprove/incoming')
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
