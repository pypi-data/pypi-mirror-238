import unittest

from src.customdataclass import Dataclass


class Parent(Dataclass):
    """Test class."""

    int_var: int
    float_var: float
    str_var: str
    bool_var: bool


class Child(Parent):
    """Test class."""

    ...


class SimpleParent(Dataclass):
    int_var: int


class ChildWithAddedAttributes(SimpleParent):
    str_var: str


class ParentWithMethods(Dataclass):
    name: str

    def greet(self) -> str:
        return f"Hello, {self.name}"


class ChildWithMethods(ParentWithMethods):
    age: int

    def greetAge(self) -> str:
        return f"Hello, {self.name}, you are {self.age} years old"


class TestAttributesInheritance(unittest.TestCase):
    def testChildCreation(self):
        c = Child(int_var=10, float_var=10.0, str_var="10", bool_var=True)
        self.assertEqual(c.int_var, 10)
        self.assertEqual(c.float_var, 10.0)
        self.assertEqual(c.str_var, "10")
        self.assertEqual(c.bool_var, True)
        self.assertIsInstance(c, Child)
        self.assertIsInstance(c, Parent)

    def testChildParentEquality(self):
        p = Parent(int_var=10, float_var=10.0, str_var="10", bool_var=True)
        c = Child(int_var=10, float_var=10.0, str_var="10", bool_var=True)
        self.assertNotEqual(c, p)

    def testChildWithAddedAttributes(self):
        c = ChildWithAddedAttributes(int_var=10, str_var="10")
        self.assertEqual(c.int_var, 10)
        self.assertEqual(c.str_var, "10")
        self.assertIsInstance(c, ChildWithAddedAttributes)
        self.assertIsInstance(c, SimpleParent)

    def testChildWithMethods(self):
        c = ChildWithMethods(name="John", age=10)
        self.assertEqual(c.name, "John")
        self.assertEqual(c.age, 10)
        self.assertEqual(c.greet(), "Hello, John")
        self.assertEqual(c.greetAge(), "Hello, John, you are 10 years old")
        self.assertIsInstance(c, ChildWithMethods)
        self.assertIsInstance(c, ParentWithMethods)
