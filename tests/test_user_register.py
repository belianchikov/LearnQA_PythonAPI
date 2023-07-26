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

        assert response.status_code == 200, f"Wrong response status code {response.status_code}"
        assert "id" in response.text, f"Unexpected response text {response.text}"

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = {
            'password': '123',
            'email': email,
            'username': 'username1',
            'firstName': 'Anatoly',
            'lastName': 'Rich'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Wrong response status code {response.status_code}"
        assert response.text == f"Users with email '{email}' already exists", f"Unexpected response text {response.text}"

    @pytest.mark.parametrize("field", fields)
    def test_create_user_without_required_fields(self, field):
        email = "vinkotov@example.com"
        data = {
            'password': '123',
            'email': email,
            'username': 'username1',
            'firstName': 'Anatoly',
            'lastName': 'Rich'
        }

        data.pop(field)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Wrong response status code {response.status_code}"
        assert response.text == f"The following required params are missed: {field}", f"Unexpected response text {response.text}"

    def test_create_user_without_at_sign(self):
        base_part = "base"
        domain = "domain.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}{domain}"

        data = {
            'password': '123',
            'email': email,
            'username': 'username1',
            'firstName': 'Anatoly',
            'lastName': 'Rich-man'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Wrong response status code {response.status_code}"
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
            'firstName': '1',
            'lastName': 'Rich-man'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Wrong response status code {response.status_code}"
        assert response.text == "The value of 'firstName' field is too short", f"Unexpected response text {response.text}"

    def test_create_user_with_long_username(self):
        base_part = "base"
        domain = "domain.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
            'password': '123',
            'email': email,
            'username': 'username1',
            'firstName': 'Далеко-далеко за словесными горами в стране гласных и согласных живут рыбные тексты. Вдали '
                         'от всех живут они в буквенных домах на берегу Семантика большого языкового океана. '
                         'Маленький ручеек Даль журчит по всей стране и обеспечивает ее всеми необходи',
            'lastName': 'Rich-man'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Wrong response status code {response.status_code}"
        assert response.text == "The value of 'firstName' field is too long", f"Unexpected response text {response.text}"