from webdav3.client import Client
options = {
 #'webdav_hostname': "https://fasolt4.willab.fi:8883/dav/",
 'webdav_hostname': "http://192.168.0.114:8081/remote.php/dav/files/tai/",
 'webdav_login':    "tai",
 'webdav_password': "zuggo6pullo3",
 'disable_check': True
 #'webdav_override_methods': {'check': 'GET'}
}
client=Client(options)
client.verify=False

#print(client.list("common-files"))
#client.execute_request("mkdir", "personal-files/paskaa")
#client.list('/personal-files/')
print(client.list())