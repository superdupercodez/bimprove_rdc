import requests
import pprint

domain = 'https://fasolt4.willab.fi:8883'
#domain = 'http://192.168.0.114:8080'
user = 'bimuser'
password = 'bimproveK0ukku55'
#user = 'admin'
#password = 'K0ukku55'

# These will be the same for all requests/responses.
_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

# Create an http session.
client = requests.Session()
#client.headers['User-Agent'] = _headers['User-Agent']

# Login
login_data =  {'AuthInfo': {'login': user, 'password': password, 'type': 'credentials'}}
r = client.post(domain+'/a/frontend/session', json=login_data, verify=False, headers=_headers)

# a valid JWT token should be found in the returned JSON object ...

jwt_token = r.json()['JWT']
jwt_expire = r.json()['ExpireTime']  # in seconds

 # Add this to headers
print(f"This token will expire in {jwt_expire} seconds")
_headers2 = {}
_headers2['Content-Type'] = 'application/json'
_headers2['Authorization'] = 'Bearer {}'.format(jwt_token)
_headers2['Cache-Control'] = 'no-cache'

#3fe544e7-f485-43e2-b176-1b61a3a5da26
#'Slug': 'bimprove-image-storage'

#result = requests.post(domain+'/a/tree/stats', json={'NodePaths' : ['bimprove-image-storage/processed/*'] }, verify=False, headers=_headers2)

#result = requests.post(domain+'/a/workspace', json={'Queries' : [{'label':'20-1.jpg'}]}, verify=False, headers=_headers2)
#result = requests.post(domain+'/a/workspace', json={}, verify=False, headers=_headers2)

#result = requests.post('https://fasolt4.willab.fi:8883/a/share/resources', json={'Limit': 1000}, verify=False, headers=_headers2)
#pprint.pprint(result.json())


#result = requests.get(domain+"/a/tree/stat/bimprove-image-storage/processed/bbxes_20-1.jpg", verify=False, headers=_headers2)
#pprint.pprint(result.json())
#result = requests.get(domain+"/a/share/cell/e0bdf9ec-3938-4743-8200-87f7aa99eaae", verify=False, headers=_headers2)

#result = requests.get(domain+"/a/share/link/f42d48bd-2ac9-4bbd-b9db-3d046991f7c4", verify=False, headers=_headers2)
result = requests.get(domain+"/a/share/link/9934c40c-04bf-11ec-8fb0-008cfa000868", verify=False, headers=_headers2)

pprint.pprint(result.json())

#p = { 'ShareLink' : {'Label' : 'Stuff', 'RootNodes' : [{'Uuid' : '50168ba5-be65-43a3-91c4-736956919e8c'}]} }
#result = requests.put(domain+"/a/share/link", json=p, verify=False, headers=_headers2)
#print(result)
#pprint.pprint(result.text)
