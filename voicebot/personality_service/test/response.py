import requests
r = requests.get('http://localhost:4000/personality-service', params={"emotion": "0.452323,0.92343434"})
print(r.status_code)
print(r.json())



