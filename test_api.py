import requests
import json
url = 'http://127.0.0.1:8000/api/v1/chat/29/'
headers = {
    'Content-Type': 'application/json'
}
data = {
    'chat':'212312',
    'name':'asdkajsdlkjasdlkj',
    'level':'1'
}
response = requests.get(url) #headers=headers, data=json.dumps(data))
print(response.status_code)  
if response.status_code == 404:
    res = requests.post('http://127.0.0.1:8000/api/v1/chat/', headers=headers, data=json.dumps(data))
    print(res.status_code)
