import time
import os
import subprocess
import glob
import pprint
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from webdav3.client import Client
from PIL import Image, ImageFont, ImageDraw

class Clunki():
    def __init__(self, **kwargs):
        self.service_host = ""
        self.image_to_bcf_url = 'http://localhost:8084/ImageToBCF'
        self._detection_service_url = "http://"+self.service_host+":5001/v1/risk_objects/"
        self._file_storage_url = "https://"+self.service_host+":8883/dav/"
        self.dav_options = {
            'webdav_hostname': self._file_storage_url,
            'webdav_login':    "",
            'webdav_password': "",
            'verbose' : True,
            'disable_check': True
        }
        self.os_incoming_path = '/var/cells/data/bimprove/incoming'
        self.os_processed_path = '/var/cells/data/bimprove/processed'
        self.os_temp_file_path = '/tmp'
        self.webdav_incoming_path = 'bimprove-image-storage/incoming'
        self.webdav_processed_path = 'bimprove-image-storage/processed'
        self.webdav_temp_path = 'bimprove-image-storage/temp'
        self.webdav_nodetections_path = 'bimprove-image-storage/nodetections'

        self.jwt_expiresat = time.time()

    def _auth_with_pydio(self):
        pydio_auth_req_header = {
			    'Content-Type': 'application/json',
			    'Accept': 'application/json',
			    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
			}

        client = requests.Session()
        user = 'bimuser'
        password = 'bimproveK0ukku55'
	# Login
        login_data =  {'AuthInfo': {'login': user, 'password': password, 'type': 'credentials'}}
        r = client.post("https://"+self.service_host+':8883/a/frontend/session', json=login_data, verify=False, headers=pydio_auth_req_header)
        # a valid JWT token should be found in the returned JSON object ...
        jwt_token = r.json()['JWT']
        self.jwt_expiresat = int(r.json()['Token']['ExpiresAt'])
        # Add this to headers
        self.pydio_auth_headers = {}
        self.pydio_auth_headers['Content-Type'] = 'application/json'
        self.pydio_auth_headers['Authorization'] = 'Bearer {}'.format(jwt_token)
        self.pydio_auth_headers['Cache-Control'] = 'no-cache'


    def _find_file_id(self, file_name):
        if self.jwt_expiresat <= time.time():
            self._auth_with_pydio()
        file_req_url = "https://"+self.service_host+":8883/a/tree/stat/bimprove-image-storage/processed/"+file_name
        trials = 0
        result = requests.models.Response()
        while result.status_code != 200:
            result = requests.get(file_req_url, verify=False, headers=self.pydio_auth_headers)
            print("FFID ", file_req_url, result)
            trials+= 1
            if trials > 5:
                break
            time.sleep(trials)
        if result.status_code == 200:
            return result.json()['Node']['Uuid']
        else:
            print(result)
            print(result.text)
        return None

    def create_share(self, file_label, file_uuid):
        share_params = { 'ShareLink' : {'Label': file_label, 'Permissions': ['Preview', 'Download'], 'ViewTemplateName': 'pydio_unique_strip', 'RootNodes' : [{'Uuid' : file_uuid}]} }
        if self.jwt_expiresat <= time.time():
            self._auth_with_pydio()
        #Create share
        time.sleep(2)
        file_share_req_url = "https://"+self.service_host+":8883/a/share/link"
        result = requests.models.Response()
        trials = 0
        while result.status_code != 200:
            result = requests.put(file_share_req_url, json=share_params, verify=False, headers=self.pydio_auth_headers)
            print("CrFS ", file_share_req_url, result)
            trials+=1
            if trials > 5:
                return None
            time.sleep(trials)
        if result.status_code == 200:
            return result.json()['LinkUrl']
        else:
            print(result)
            print(result.text)
        return None

    def insert_to_BCF_db(self, file_name, new_file_name, detections):
        uuid = self._find_file_id(file_name)
        nf_uuid = self._find_file_id(new_file_name)

        print("Attempting to insert to BCF")

        if uuid is not None:
            file_share_url = self.create_share(file_name, uuid)
        if nf_uuid is not None:
            new_file_share_url = self.create_share(new_file_name, nf_uuid)
        print("Something ought to happen soon...", uuid, nf_uuid)

        if uuid is not None and nf_uuid is not None:
            _header = {'Content-Type': 'text/plain'}
            if file_share_url is not None:
                full_imgUrl = str('https://'+self.service_host+':8883'+file_share_url)
            if new_file_share_url is not None:
                full_new_imgUrl = str('https://'+self.service_host+':8883'+new_file_share_url)

            for detection in detections:
                _json_content = {'imageID': str(file_name + "_" +uuid),
                                 'name': detection['name'],
                                 'confidence': str(detection['confidence']),
                                 'xmax': str(detection['xmax']),
                                 'xmin': str(detection['xmin']),
                                 'ymax': str(detection['ymax']),
                                 'ymin': str(detection['ymin']),
                                 'imageURL': full_imgUrl,
                                 'anchorBoxImageURL': full_new_imgUrl}
                print(_json_content)
                resp = requests.post(self.image_to_bcf_url, verify=False, json=_json_content, headers=_header)
                if resp.status_code != 200:
                    print(f"Insertion to BCF failed with {resp.status_code}:{resp.text}")
                else:
                    print(f"Insertion to BCF succeedes(?) with {resp.status_code}:{resp.text}")

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
            print(f"Saving {os_file_path} as new image file {new_full_file_name} - basefile name is {base_file_name}")
            #img.save(new_full_file_name, "JPEG")
	    if 'exif' in img.info.keys():
                img.save(new_full_file_name, exif=img.info['exif'])
            else:
                img.save(new_full_file_name)
            return new_full_file_name, detections
        return None, None

    def sync_pydio(self):
        print("Trying to sync pydio thingy")
        pwd='429Memfw'
        cmd='docker exec a4a93170a819 cells admin resync --datasource=bimprove'
        subprocess.call('echo {} | sudo -S {}'.format(pwd,cmd), shell=True)

    def move_files(self, file_os_path, new_file_os_path):
        #Extract file name from the OS file path
        file_name = file_os_path.replace(self.os_incoming_path+'/', '')
        new_file_name = new_file_os_path.replace(self.os_temp_file_path+'/', '')
        pyd_file_name = None
        pyd_new_file_name = None
        timex = str(int(time.time()))
        print(f"Trying to move {file_os_path} and {new_file_os_path}: {file_name} and {new_file_name}")
        if len(file_name) > 0 and len(new_file_name) > 0:
            client=Client(self.dav_options)
            client.verify=False
            if file_name in client.list(self.webdav_incoming_path):
                pyd_file_name = timex + "_" + file_name
                print(f"Moving the original file from incoming to processed {file_name}, new file name {pyd_file_name}")
                client.move(remote_path_from=self.webdav_incoming_path+'/'+file_name, remote_path_to=self.webdav_processed_path+'/'+pyd_file_name)
            else:
                print(f"TILT file {file_name} not found")
            pyd_new_file_name = timex + "_" + new_file_name
            print(f"Uploading the bounding box image version from {new_file_os_path} to procssed as {pyd_new_file_name}")
            if os.path.exists(new_file_os_path):
                print("File found from tmp to be moved")
                client.upload_sync(local_path=new_file_os_path, remote_path=self.webdav_processed_path+"/"+pyd_new_file_name)
                print("File upload from tmp done")
                #Delete files from tmp
                os.remove(new_file_os_path)
                self.sync_pydio()
                return pyd_file_name, pyd_new_file_name
            self.sync_pydio()
            return pyd_file_name, None
        self.sync_pydio()
        return None, None

    def do_inference(self, file_path):
        print("Doing inferencing..")
        image_data = open(file_path, "rb").read()
        response = requests.post(self._detection_service_url, files={"image": image_data})
        print(response)
        if len(response.json()) > 0:
            new_temp_file_and_path, detections = self.add_bounding_box_to_img(file_path, response.json())
            pprint.pprint(response.json())
            file_name, new_file_name = self.move_files(file_path, new_temp_file_and_path)
            print("Inference done, files moved: old name: ",file_name, " new name: ", new_file_name)
            if file_name is not None and new_file_name is not None and detections is not None:
                self.insert_to_BCF_db(file_name, new_file_name, detections)
        #No detections - move to nodetections -folder
        else:
            client=Client(self.dav_options)
            client.verify=False
            file_name = file_path.replace(self.os_incoming_path+'/', '')
            timex = str(int(time.time()))
            client.move(remote_path_from=self.webdav_incoming_path+'/'+file_name, remote_path_to=self.webdav_nodetections_path+'/'+timex+'_'+file_name)
            self.sync_pydio()

    def on_created(self, event): # when file is created
        print("Got event for file %s" %event.src_path)
        img_ext_list = ['jpg', 'gif', 'tif', 'png', 'jpeg']
        img_ext = event.src_path.split('.')[-1]
        if img_ext.lower() in img_ext_list:
            self.do_inference(event.src_path)

    def start_file_observer(self):
        print("clink..")
        self.observer = Observer()
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_created = self.on_created
        self.observer.schedule(self.event_handler, path=self.os_incoming_path)
        self.observer.start()
        print("..clonk")

if __name__ == "__main__":
    clunk = Clunki()
    print("Clunketi clunk..")
    clunk.start_file_observer()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        clunk.observer.stop()
    clunk.observer.join()
