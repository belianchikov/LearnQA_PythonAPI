from json.decoder import JSONDecodeError
import requests

response = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=True)

print(response.history[0].status_code)
print(response.history[0].url)

print(response.status_code)
print(response.url)