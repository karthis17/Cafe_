import requests
response = requests.get("https://cafe-yuk2.onrender.com/all")

for i in response.json()['cafe']:
    print(type(response.json()['cafe'][i]))