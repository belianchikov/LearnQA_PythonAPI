import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User edit cases")
class TestUserEdit(BaseCase):
    @allure.description("Deleting just created user")
    def test_user_edit_just_created(self):
        # Registration
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = register_data["email"]
        password = register_data["password"]

        # Login
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_name = "Is it new Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        # Check
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong user name after edit")

    @allure.description("Trying to edit user not authorized")
    def test_user_edit_not_authorised(self):
        # Registration
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # Login skip

        # Edit with no auth token
        new_name = "Is it new Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   data={"firstName": new_name})

        assert response3.text == "Auth token not supplied"
        Assertions.assert_code_status(response3, 400)

    @allure.description("Truing to edit user authorized as another user")
    def test_user_edit_authorised_as_another_user(self):
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
        second_user_firstname = second_user_register_data["firstName"]

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

        # Edit second username with first user login data
        new_name_for_second_user = "Is it new Name"

        response5 = MyRequests.put(f"/user/{second_user_user_id}",
                                   headers={"x-csrf-token": first_user_token},
                                   cookies={"auth_sid": first_user_auth_sid},
                                   data={"firstName": new_name_for_second_user})

        Assertions.assert_code_status(response5, 200)

        # Check second username with second user login data
        response6 = MyRequests.get(f"/user/{second_user_user_id}",
                                   headers={"x-csrf-token": second_user_token},
                                   cookies={"auth_sid": second_user_auth_sid})

        Assertions.assert_json_value_by_name(response6, "firstName", second_user_firstname,
                                             "User name changed by request with wrong login data")

    @allure.description("Trying to edit user's email to new email without @ sign")
    def test_user_edit_email_without_at_sign(self):
        # Registration
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        old_email = register_data["email"]
        password = register_data["password"]

        # Login
        login_data = {
            "email": old_email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_email = old_email.replace('@', '')

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email})

        Assertions.assert_code_status(response3, 400)
        assert response3.text == "Invalid email format", f"Email changed for new one with no at sign"
        # Check
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4, "email", old_email, "Email changed for new one with no at sign")

    @allure.description("Trying to edit user's firstname to new one with one character")
    def test_user_edit_short_firstname(self):
        # Registration
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = register_data["email"]
        password = register_data["password"]
        old_first_name = register_data["firstName"]

        # Login
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_first_name = "a"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_first_name})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error",
                                             "Too short value for field firstName",
                                             f"Wrong name change to short name")

        # Check
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", old_first_name, "Wrong name change to short name")
