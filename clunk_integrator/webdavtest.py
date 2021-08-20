from webdav3.client import Client
options = {
 'webdav_hostname': "http://192.168.0.114:8080/dav/",
 'webdav_login':    "admin",
 'webdav_password': "429Memfw",
 'disable_check': True
 #'webdav_override_methods': {'check': 'GET'}
}
client=Client(options)
client.verify=False

#print(client.list("common-files"))
#client.execute_request("mkdir", "personal-files/paskaa")
#client.list('/personal-files/')
print(client.list())
print(client.list("/personal-files/"))
#client.move(remote_path_from="dir1/file1", remote_path_to="dir2/file1")
client.move(remote_path_from="/personal-files/bouty.jpg", remote_path_to="/personal-files/test/bouty.jpg")
print(client.list("/personal-files/test/"))