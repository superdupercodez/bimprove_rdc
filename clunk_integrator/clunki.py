import time
import pprint
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        print("Got event for file %s" %event.src_path)
        img_ext_list = ['jpg', 'gif', 'tif', 'png']
        img_ext = event.src_path.split('.')[-1]
        if img_ext.lower() in img_ext_list:
            image_data = open(event.src_path, "rb").read()
            response = requests.post(DETECTION_URL, files={"image": image_data}).json()
            pprint.pprint(response)

DETECTION_URL = "http://localhost:5001/v1/risk_objects/"
observer = Observer()
event_handler = ExampleHandler() # create event handler

# set observer to use created handler in directory
observer.schedule(event_handler, path='/var/cells/data/bimprove/incoming')
observer.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
