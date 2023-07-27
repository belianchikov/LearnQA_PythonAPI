from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}"

        assert name in response_as_dict, f"Response JSON does not have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}"

        assert name in response_as_dict, f"Response JSON does not have key '{name}'"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert expected_status_code == response.status_code, \
            f"Unexpected status code. Expected: {expected_status_code}. Actual: {response.status_code}."


