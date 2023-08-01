from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_user_delete_successfully(self):
        # Registration
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = register_data["email"]
        password = register_data["password"]
        print(user_id)

        # Login
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # User deleting
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)

        # Check, that user was deleted
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found", \
            f"Unexpected text after successfully user delete. Text is '{response4.text}'"

    def test_user_delete_with_id_2(self):
        # Login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Delete
        response2 = MyRequests.delete(f"/user/2",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400)
        assert response2.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            "Wrong message for deleting user with id = 2"

        # Check, that user was not deleted
        response3 = MyRequests.get("/user/2",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_keys(response3, ["id", "username", "email", "firstName", "lastName"])

    def test_user_delete_logged_as_another_user(self):
        # User #1 registration
        first_user_register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user", data=first_user_register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_user_email = first_user_register_data["email"]
        first_user_password = first_user_register_data["password"]

        # User #2 registration
        second_user_register_data = self.prepare_registration_data()

        response2 = MyRequests.post("/user", data=second_user_register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        second_user_user_id = self.get_json_value(response2, "id")
        second_user_email = second_user_register_data["email"]
        second_user_password = second_user_register_data["password"]

        # First user login
        first_user_login_data = {
            "email": first_user_email,
            "password": first_user_password
        }

        response3 = MyRequests.post("/user/login", data=first_user_login_data)

        first_user_auth_sid = self.get_cookie(response3, "auth_sid")
        first_user_token = self.get_header(response3, "x-csrf-token")

        # Second user login
        second_user_login_data = {
            "email": second_user_email,
            "password": second_user_password
        }

        response4 = MyRequests.post("/user/login", data=second_user_login_data)

        second_user_auth_sid = self.get_cookie(response4, "auth_sid")
        second_user_token = self.get_header(response4, "x-csrf-token")

        # Try to delete user#2 with user#1 login data
        response5 = MyRequests.delete(f"/user/{second_user_user_id}",
                                      headers={"x-csrf-token": first_user_token},
                                      cookies={"auth_sid": first_user_auth_sid})

        Assertions.assert_code_status(response5, 200)  # but why 200?

        # Check, that user#2 was not deleted
        response6 = MyRequests.get(f"/user/{second_user_user_id}",
                                   headers={"x-csrf-token": second_user_token},
                                   cookies={"auth_sid": second_user_auth_sid})

        Assertions.assert_code_status(response6, 200)
        Assertions.assert_json_has_keys(response6, ["id", "username", "email", "firstName", "lastName"])
