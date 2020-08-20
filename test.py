import requests

url = "http://0.0.0.0:8062/post_processing_religion"


#payload = "{\"name\"😕"LTr TD HCM\"}"
payload = "{\"name\":\"Nao Vei\"}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
