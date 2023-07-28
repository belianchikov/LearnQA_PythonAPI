from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest

from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    fields = [
        "password",
        "email",
        "username",
        "firstName",
        "lastName"
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"Users with email '{email}' already exists", \
            f"Unexpected response text {response.text}"

    @pytest.mark.parametrize("field", fields)
    def test_create_user_without_required_fields(self, field):
        data = self.prepare_registration_data()

        data.pop(field)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"The following required params are missed: {field}", \
            f"Unexpected response text {response.text}"

    def test_create_user_without_at_sign(self):
        data = self.prepare_registration_data()
        data["email"] = data["email"].replace('@', '')

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "Invalid email format", f"Unexpected response text {response.text}"

    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data["firstName"] = "1"

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'firstName' field is too short", \
            f"Unexpected response text {response.text}"

    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        data["firstName"] = "Далеко-далеко за словесными горами в стране гласных и согласных живут рыбные " \
                                 "тексты. Вдали от всех живут они в буквенных домах на берегу Семантика большого " \
                                 "языкового океана. Маленький ручеек Даль журчит по всей стране и обеспечивает ее " \
                                 "всеми необходи"

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'firstName' field is too long", f"Unexpected response text {response.text}"
