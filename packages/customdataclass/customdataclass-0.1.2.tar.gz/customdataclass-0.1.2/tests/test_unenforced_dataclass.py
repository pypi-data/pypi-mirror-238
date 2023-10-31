from src.customdataclass import Dataclass

import unittest


class UnenforcedDataclass(Dataclass, enforce_types=False):
    field_a: int
    field_b: str
    field_c: list[str]


class TestUnenforcedDataclass(unittest.TestCase):
    def testCorrectTypes(self):
        u = UnenforcedDataclass(field_a=1, field_b="1", field_c=["1", "2", "3"])
        self.assertEqual(u.field_a, 1)
        self.assertEqual(u.field_b, "1")
        self.assertEqual(u.field_c, ["1", "2", "3"])

        self.assertIsInstance(u.field_a, int)
        self.assertIsInstance(u.field_b, str)
        self.assertIsInstance(u.field_c, list)

    def testIncorrectTypes(self):
        u = UnenforcedDataclass(field_a="1", field_b=1, field_c={1, 2, 3})
        self.assertEqual(u.field_a, "1")
        self.assertEqual(u.field_b, 1)
        self.assertEqual(u.field_c, {1, 2, 3})

        self.assertIsInstance(u.field_a, str)
        self.assertIsInstance(u.field_b, int)
        self.assertIsInstance(u.field_c, set)
