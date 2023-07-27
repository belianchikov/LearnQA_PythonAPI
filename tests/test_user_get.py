import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import pytest


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")

        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "firstName", "lastName", "email"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_different_user(self):
        base_part = "base"
        domain = "domain.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
            'password': '123',
            'email': email,
            'username': 'username15',
            'firstName': 'Anatoly',
            'lastName': 'Rich-man'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        created_user_id = self.get_json_value(response1, "id")

        data2 = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data2)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = requests.get(f"https://playground.learnqa.ru/api/user/{created_user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_json_has_key(response3, "username")
        Assertions.assert_json_has_no_key(response3, "email")
        Assertions.assert_json_has_no_key(response3, "firstName")
        Assertions.assert_json_has_no_key(response3, "lastName")
