import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

for i in range(len(response.history)):
    print(response.history[i].status_code)
    print(response.history[i].url)

print(response.status_code)
print(response.url)