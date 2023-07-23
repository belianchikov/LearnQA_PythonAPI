import requests


class TestHeaders():
    def test_header_for_secret_value(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)
        expected_header_value = "Some secret value"
        actual_header_value = response.headers.get("x-secret-homework-header")

        assert expected_header_value == actual_header_value, f"Actual header value is not equal to {expected_header_value}"