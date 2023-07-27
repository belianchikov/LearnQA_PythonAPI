import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import pytest


class TestUserRegister(BaseCase):
    fields = [
        "password",
        "email",
        "username",
        "firstName",
        "lastName"
    ]

    def test_create_user_successfully(self):
        base_part = "base"
        domain = "domain.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
            'password': '123',
            'email': email,
            'username': 'username1',
            'firstName': 'Anatoly',
            'lastName': 'Rich-man'
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"

        data = {
            'password': '123',
            'email': email,
            'username': 'username1',
            'firstName': 'Anatoly',
            'lastName': 'Rich-man'
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"Users with email '{email}' already exists", f"Unexpected response text {response.text}"

    @pytest.mark.parametrize("field", fields)
    def test_create_user_without_required_fields(self, field):
        base_part = "base"
        domain = "domain.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
            'password': '123',
            'email': email,
            'username': 'username1',
            'firstName': 'Anatoly',
            'lastName': 'Rich-man'
        }

        data.pop(field)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"The following required params are missed: {field}", \
            f"Unexpected response text {response.text}"

    def test_create_user_without_at_sign(self):
        base_part = "base"
        domain = "domain.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email_without_at_sign = f"{base_part}{random_part}{domain}"

        data = {
            'password': '123',
            'email': email_without_at_sign,
            'username': 'username1',
            'firstName': 'Anatoly',
            'lastName': 'Rich-man'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "Invalid email format", f"Unexpected response text {response.text}"

    def test_create_user_with_short_username(self):
        base_part = "base"
        domain = "domain.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
            'password': '123',
            'email': email,
            'username': 'username1',
            'firstName': 'Anatoly',
            'lastName': 'Rich-man'
        }

        data["firstName"] = "1"

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'firstName' field is too short", \
            f"Unexpected response text {response.text}"

    def test_create_user_with_long_username(self):
        base_part = "base"
        domain = "domain.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
            'password': '123',
            'email': email,
            'username': 'username1',
            'firstName': 'Anatoly',
            'lastName': 'Rich-man'
        }

        data["firstName"] = "Далеко-далеко за словесными горами в стране гласных и согласных живут рыбные " \
                                 "тексты. Вдали от всех живут они в буквенных домах на берегу Семантика большого " \
                                 "языкового океана. Маленький ручеек Даль журчит по всей стране и обеспечивает ее " \
                                 "всеми необходи"

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'firstName' field is too long", f"Unexpected response text {response.text}"
