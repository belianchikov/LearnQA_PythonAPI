import requests

response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")

print("POST-request without method param:\n", response.text)

wrong_payload = {"method": "POST123"}

response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", params=wrong_payload)

print("Wrong HEAD-request:\n", response.text)

correct_payload = {"method": "PUT"}

response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params=correct_payload)

print("Correct PUT-request:\n", response.text)

payloads = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}, {"method": "HEAD"}]

print("\nGET-request with params")
for i in range(5):
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payloads[i])
    print(payloads[i], " ", response.text)

print("\nGET-request with data")
for i in range(5):
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payloads[i])
    print(payloads[i], " ", response.text)

print("\nPOST-request with params")
for i in range(5):
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payloads[i])
    print(payloads[i], " ", response.text)

print("\nPOST-request with data")
for i in range(5):
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payloads[i])
    print(payloads[i], " ", response.text)

print("\nPUT-request with params")
for i in range(5):
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payloads[i])
    print(payloads[i], " ", response.text)

print("\nPUT-request with data")
for i in range(5):
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payloads[i])
    print(payloads[i], " ", response.text)

print("\nDELETE-request with params")
for i in range(5):
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payloads[i])
    print(payloads[i], " ", response.text)

print("\nDELETE-request with data")
for i in range(5):
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payloads[i])
    print(payloads[i], " ", response.text)

print("\nHEAD-request with params")
for i in range(5):
    response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payloads[i])
    print(payloads[i], " ", response.text)

print("\nHEAD-request with data")
for i in range(5):
    response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payloads[i])
    print(payloads[i], " ", response.text)