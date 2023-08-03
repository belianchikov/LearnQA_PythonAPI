import requests


class TestCookie:
    def test_hw_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        # print(response.cookies)
        expected_cookie_value = "hw_value"
        actual_cookie_value = response.cookies.get("HomeWork")

        assert actual_cookie_value == expected_cookie_value, f"Actual cookie value is not equal to {expected_cookie_value}"