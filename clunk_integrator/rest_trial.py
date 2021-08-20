import requests
import pprint

URL = "https://fasolt4.willab.fi:8883"

#Get token by docker exec -it a4a93170a819 cells admin user token -u admin -e 1000d
# -H 'Authorization: Bearer k87prIZsqfMoelu2oS7sis0B08RkHfCTTYmqR1d9WvI.44Vs-_JdMvKqJxf4LwpF7Ry44sxVogTWQGvieSkaBJg' 
#-H 'Cache-Control: no-cache'
headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer LHr_zc-yWv_HcWcVEdQqJa99sTZ7RCeZ1eE7zNtkxWM.lcPyrFyD0QQ9LgTt-jTMp0R9BTSJ5ZZoWHxXrGK-gs4',
            'Cache-Control': 'no-cache',
          }

#response = requests.get(URL+"/a/user/bimuser", verify=False, headers=headers)

response = requests.post(URL+"/a/tree/stats", json={ } ,verify=False, headers=headers)


pprint.pprint(response.json())
print(response.request.headers)
print(response.request.body)