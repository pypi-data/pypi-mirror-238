import unittest

from src.customdataclass import Dataclass


class BaseClass:
    pass


class SubClass(BaseClass):
    pass


class DataclassSubclassField(Dataclass):
    field: SubClass


class TestSubclassField(unittest.TestCase):
    def testSubClassField(self):
        instance = DataclassSubclassField(field=SubClass())
        self.assertIsInstance(instance.field, SubClass)
        self.assertIsInstance(instance.field, BaseClass)
