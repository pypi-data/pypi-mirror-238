import unittest

from textwrap import dedent

from cedarpy_conversor import convert_json_to_cedar_policies

class ConvertJsonToPolicyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_policy_json_to_cedar(self):
        input_policy = dedent("""
            {
                "effect": "permit",
                "principal": {
                    "op": "==",
                    "entity": { "type": "User", "id": "12UA45" }
                },
                "action": {
                    "op": "==",
                    "entity": { "type": "Action", "id": "view" }
                },
                "resource": {
                    "op": "in",
                    "entity": { "type": "Folder", "id": "abc" }
                },
                "conditions": [
                    {
                        "kind": "when",
                        "body": {
                            "==": {
                                "left": {
                                    ".": {
                                        "left": {
                                            "Var": "context"
                                        },
                                        "attr": "tls_version"
                                    }
                                },
                                "right": {
                                    "Value": "1.3"
                                }
                            }
                        }
                    }
                ]
            }
        """).strip()

        expect_result = dedent("""
            permit(
              principal == User::"12UA45",
              action == Action::"view",
              resource in Folder::"abc"
            ) when {
              (context["tls_version"]) == "1.3"
            };
        """).strip()

        actual_result = convert_json_to_cedar_policies(input_policy)

        self.assertEqual(expect_result, actual_result)
