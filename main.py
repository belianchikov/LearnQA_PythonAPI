import requests
import json
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

print(response.text)

token = json.loads(response.text)["token"]
seconds = json.loads(response.text)["seconds"]
print("token is :", token)
print("sleep for ", seconds-2, " seconds")

time.sleep(seconds-2)

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})

print(response.text)
if json.loads(response.text)["status"] == "Job is NOT ready":
    print("OK")
else:
    print("Error")

print("sleep for another two seconds")
time.sleep(2)

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})

print(response.text)
if (json.loads(response.text)["status"] == "Job is ready") & ("result" in json.loads(response.text)):
    print("OK")
else:
    print("Error")