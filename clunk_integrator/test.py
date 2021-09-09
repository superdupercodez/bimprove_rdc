from webdav3.client import Client

_service_host = "fasolt4.willab.fi"
_file_storage_url = "https://"+_service_host+":8883/dav/"
dav_options = {
    'webdav_hostname': _file_storage_url,
    'webdav_login':    "bimuser",
    'webdav_password': "bimproveK0ukku55",
    'disable_check': True
    }

client=Client(dav_options)
client.verify=False
print(client.list('bimprove-image-storage/temp'))