import unittest

from src.customdataclass import Dataclass


class NoneDataclass(Dataclass):
    """Test class."""

    nullable_int_var: int | None
    nullable_int_var_2: int | None


class TestNoneDataclass(unittest.TestCase):
    def testInstance(self):
        s1 = NoneDataclass(nullable_int_var=None, nullable_int_var_2=None)
        self.assertIsNone(s1.nullable_int_var)
        s2 = NoneDataclass(nullable_int_var=1, nullable_int_var_2=1)
        self.assertEqual(s2.nullable_int_var, 1)

    def testInvalidType(self):
        with self.assertRaises(TypeError):
            NoneDataclass(nullable_int_var="1", nullable_int_var_2=None)
        with self.assertRaises(TypeError):
            NoneDataclass(nullable_int_var=None, nullable_int_var_2="1")
