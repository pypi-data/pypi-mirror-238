import unittest
from DictMaper import MapDict


class TestGenerateMaper(unittest.TestCase):
    def test_generate_maper(self):
        result = MapDict(
            output={
                "{var_1}": "Hi! {var_2}, welcome to {company_name}",
                "company": "{company_name}"
            },
            context={
                "user": {
                    "name": "user name",
                    "email": "test_email@..."
                },
                "company": {
                    "information": {
                        "name": "Company name",
                        "id": "1234"
                    }
                }
            },
            vars={
                "var_1": "user.email",
                "var_2": "user.name",
                "company_name": "company.information.name"
            }

        )
        dict_expect = {
            "test_email@...": "Hi! user name, welcome to Company name",
            "company": "Company name"
        }
        self.assertDictEqual(result.process(), dict_expect)
