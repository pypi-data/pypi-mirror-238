import unittest

from textwrap import dedent

from cedarpy_conversor import get_entity_type_and_id

class GetEntityTypeAndIDnTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_get_entity_type_and_id(self):
        input_entity = dedent("""
          Foo::Bar::"george"
        """).strip()

        expect_result = {'entity_id': 'george', 'entity_type': 'Foo::Bar'}
        actual_result = get_entity_type_and_id(input_entity)

        self.assertEqual(expect_result, actual_result.__dict__)
