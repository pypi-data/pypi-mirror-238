"""This module contains a custom dataclass object.

It does work kinda good.
"""

from __future__ import annotations

import types
from functools import cached_property
from typing import Any

import toml
import ujson
import yaml


class Dataclass:
    """Custom dataclass.

    The real reason is that I didn't really like the way dataclasses work,
    and I wanted to have a better control over the attributes.

    Instead of using the decorator, the a Dataclass must be initialized
    by inheriting from it and specifying the attributes in the class definition.

    This simplifies the code, allowing a better control over the attributes
    and the methods.

    Check the examples folder for more information.

    Initialization parameters:
        enforce_types (bool, optional): If True, the types of the attributes
            are enforced. Defaults to True.
        frozen (bool, optional): If True, attributes cannot be changed after
            initialization. Defaults to True
        partial (bool, optional): If True, parameters can be missing in the
            initialization. Defaults to False.
    """

    _frozen: bool = False  # the class is frozen and cannot be changed
    _frozen_after_init: bool = True  # the class is frozen after initialization
    _enforce_types: bool = True  # the types of the attributes are enforced
    _partial: bool = False  # the class can be initialized with missing attributes
    _deserialized: bool = False  # the class is being deserialized
    _serializer: str | None = None  # the serializer used

    def __init__(self, **kwargs) -> Dataclass:
        """Create a new Dataclass.

        Raises:
            AttributeError: an invalid attribute is passed
            AttributeError: an attribute is missing in kwargs.
            TypeError: a value is not of the correct type.
        """
        # unfreeze the class for the initialisation
        self._frozen = False

        # check if all the attributes are valid
        self._checkAttributesValid(kwargs)
        # set the default values
        self._setDefaultValues(kwargs)

        for k, v in self.__class_attributes__.items():
            # skip the loop if partial is True and the attribute is not present
            if self._deserialized and self._enforce_types:
                # serialized format don't support tuple and set (they convert
                # both to list), so we need to convert them back IMPLICITLY
                if self._checkDeserializedIterator(kwargs[k], v):
                    # convert to tuple or set
                    kwargs[k] = self._deserializeOperator(kwargs[k], v)

                # serialised format don't support classes (they convert them to
                # dict), so we need to convert them back IMPLICITLY
                elif self._checkDeserializedClass(kwargs[k], v):
                    # convert to class
                    class_type, is_list = self._getDeserializedClass(v)
                    kwargs[k] = self._deserializeClass(kwargs[k], class_type, is_list)

            # check that the type is correct
            current_value = kwargs.get(k, None)
            if self._enforce_types:
                correct_type = self._checkTypeCorrect(current_value, v)
            else:
                correct_type = True
            # the type is not correct if:
            #   - the class is partial, the current value is not None,
            #       the types are enforced and the type is not correct
            #   - the class is not partial and the type is not correct
            raise_condition = (
                self._partial
                and current_value is not None
                and self._enforce_types
                and not correct_type
            ) or (not self._partial and not correct_type and self._enforce_types)

            if raise_condition:
                types = ", ".join(t.__name__ for t in v)
                raise TypeError(f"{k} should be {types}, not {current_value.__class__}")

            setattr(self, k, current_value)

        # freeze the class
        self._frozen = self._frozen_after_init
        # unset the deserialized flag
        self._deserialized = False

    def freeze(
        self,
    ) -> None:
        """Freeze the class.

        After this, attributes cannot be changed.
        The action cannot be undone.
        """
        self._frozen = True

    def _checkAttributesValid(self, kwargs: dict) -> bool:
        """Check if all the attributes are valid (as specified in the class \
            definition).

        Args:
            kwargs (dict): kwargs to check

        Returns:
            bool: True if all the attributes are valid, False otherwise.
        """
        for k in kwargs.keys():
            if k not in self.__class_attributes__.keys():
                raise AttributeError(f"{k} is not a valid attribute")

        return True

    def _setDefaultValues(self, kwargs: dict) -> None:
        """Set the default values for the attributes.

        Args:
            kwargs (dict): kwargs to check
        """
        for k in self.__class_attributes__:
            if k not in kwargs:
                try:
                    default_value = self.__getattribute__(k)
                except AttributeError:
                    if self._partial:
                        default_value = None
                    else:
                        raise AttributeError(f"Missing {k} in kwargs")

                kwargs[k] = default_value

    def _checkTypeCorrect(self, value: Any, valid_type: tuple[type]) -> bool:
        """Check if the type of the value is correct.

        Args:
            value (Any): value to check
            valid_type (tuple[type]): tuple of valid types

        Returns:
            bool: True if the type is correct, False otherwise.
        """
        if Any in valid_type:
            return True
        if value is None:
            return any(t == types.NoneType for t in valid_type)

        def check_type(value, type: Any) -> bool:
            # if the type has the __origin__ attribute, it's a generic type
            if hasattr(type, "__origin__"):
                if type.__origin__ is dict:
                    # check if the type is a dict of the specified type
                    for k in value:
                        for t in type.__args__:
                            if check_type(k, t):
                                return True
            try:
                # isinstance doesn't work with generic types
                return isinstance(value, type)
            except TypeError:
                # check if the type is a tuple of the specified type
                for i, t in enumerate(type.__args__):
                    if check_type(value[i], t):
                        return True

        # at least one of the types must be correct
        return any(check_type(value, t) for t in valid_type)

    def _deserializeOperator(
        self, value: list[Any], valid_type: tuple[type]
    ) -> set[Any] | tuple[Any] | list[Any]:
        """Return the deserialized iterator.

        Args:
            value (list[Any]): value to check
            valid_type (type): type of the value

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        class_type = next(t for t in valid_type if t is not None)
        return class_type(value)

    def _checkDeserializedIterator(self, value: list[Any], valid_type: type) -> bool:
        """Check if the value is a deserialized iterator.

        JSON, TOML and YAML convert sets and tuples to lists, so we need to
        convert them back.

        Args:
            value (list[Any]): value to check
            valid_type (type): type of the value

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        if isinstance(value, list):
            if list in valid_type:
                return False
            if any(t in valid_type for t in (tuple, set)):
                return True
        # if value is not a list, then there's no need to convert it
        return False

    def _deserializeClass(
        self, value: dict | list[dict], valid_type: type, is_list: bool
    ) -> list[Dataclass] | Dataclass:
        """Check if the value is a deserialized class.

        JSON, TOML and YAML convert classes to dicts, so we need to
        convert them back.
        Since both lists of dictionaries and single dictionaries
        can be instances of Dataclass objects (or subclasses of Dataclass),
        we need to check if the value is a list or not.

        Args:
            value (dict | list[dict]): value to check
            valid_type (type): type of the value

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        # a list of Dataclass is converted to a list
        # a single Dataclass is converted to a dict
        if is_list:
            return [valid_type.from_dict(i) for i in value]

        return valid_type.from_dict(value)

    def _getDeserializedClass(self, valid_type: tuple[type]) -> tuple[type, bool]:
        """Return the deserialized class.

        Objects

        Args:
            valid_type (tuple[type]): type of the value

        Returns:
            tuple[type, bool]: type of the value and if it's a list
        """
        convert_class = next(t for t in valid_type if t is not None)
        if hasattr(convert_class, "__origin__") and convert_class.__origin__ is list:
            inner_class = next(t for t in convert_class.__args__ if t is not None)
            return inner_class, True

        return convert_class, False

    def _checkDeserializedClass(self, value: dict, valid_type: tuple[type]) -> bool:
        """Check if the value is a valid class.

        Args:
            value (dict): value to check
            valid_type (type): type of the value

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        # a list of Dataclass is converted to a list
        # a single Dataclass is converted to a dict
        if not isinstance(value, dict) and not isinstance(value, list):
            return False

        if isinstance(value, dict):
            return any(issubclass(t, Dataclass) for t in valid_type)

        if isinstance(value, list):
            for i in value:
                if not isinstance(i, dict):
                    return False

            for t in valid_type:
                if hasattr(t, "__origin__") and t.__origin__ is list:
                    return any(issubclass(t, Dataclass) for t in t.__args__)

        return False

    def __init_subclass__(
        cls,
        enforce_types: bool = True,
        frozen: bool = True,
        partial: bool = False,
        **kwargs,
    ) -> None:
        """Initialize the subclass.

        Args:
            enforce_types (bool, optional): If True, the types of the attributes
                are enforced. Defaults to True.
            frozen (bool, optional): If True, attributes cannot be changed after
                initialization. Defaults to True.
            partial (bool, optional): If True, the class can be initialized with
                missing attributes. Defaults to False.
        """
        cls._enforce_types = enforce_types
        cls._frozen_after_init = frozen
        cls._partial = partial
        super().__init_subclass__(**kwargs)

    def __setattr__(self, key: str, value):
        """Set an attribute.

        Args:
            key (str): name of the attribute
            value (any): value of the attribute

        Raises:
            AttributeError: Attribute is not valid
        """
        if key.startswith("_"):
            super().__setattr__(key, value)
            return

        if self._frozen:
            raise AttributeError(
                f"Can't set {key}. {self.__class__.__name__} is immutable."
            )

        super().__setattr__(key, value)

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Returns:
            str
        """
        if not self.__clean_dict__:
            return f"{self.__class__.__name__}()"

        parentheses = {
            "tuple": ("(", ")"),
            "list": ("[", "]"),
            "set": ("{", "}"),
            "dict": ("{", "}"),
        }

        s = f"{self.__class__.__name__}("

        for k, v in self.__clean_dict__.items():
            if self._partial and v is None:
                continue
            s += f"{k}="
            if isinstance(v, str):
                s += f'"{v}"'
            elif isinstance(v, (list, tuple, set, dict)):
                s += parentheses[v.__class__.__name__][0]
                if isinstance(v, dict):
                    s += ", ".join(f'"{k}": {v}' for k, v in v.items())
                else:
                    s += f"{', '.join(str(i) for i in v)}"

                s += parentheses[v.__class__.__name__][1]
            else:
                s += str(v)

            s += ", "

        s = s[:-2] + ")"
        return s

    def __str__(self) -> str:
        """Return a string representation of the object.

        Returns:
            str
        """
        return self.__repr__()

    def __eq__(self, other) -> bool:
        """Compare two objects.

        Args:
            other (any): object to compare

        Returns:
            bool
        """
        if not isinstance(other, self.__class__):
            return False

        for k in self.__class_attributes__:
            if getattr(self, k) != getattr(other, k):
                return False

        return True

    def __hash__(self) -> int:
        """Return the hash of the object.

        Returns:
            int
        """
        ordered = sorted(self.__clean_dict__.items())
        return hash(tuple(ordered))

    def __contains__(self, item) -> bool:
        """Check if the object contains an item.

        This is used to check if an attribute exists via the
        built-in `in` operator.

        Args:
            item (any): item to check

        Returns:
            bool
        """
        return item in self.__clean_dict__.keys()

    def __iter__(self):
        """Return an iterator for the object.

        Returns:
            iterator
        """
        return iter(self.__clean_dict__.items())

    @cached_property
    def __class_attributes__(self) -> dict[str, type]:
        """Return all the attributes of the class and their type.

        Returns:
            dict
        """
        return self._loadAnnotationsIterative()

    def _loadAnnotationsIterative(
        self,
        current: dict[str, type] = None,
        annotations: dict[str, type] = None,
        cls: type = None,
    ) -> dict[str, type]:
        """Load the annotations of the class and its parents.

        Args:
            current (dict[str, type], optional): current annotations. Defaults to None.
            annotations (dict[str, type], optional): annotations of the current class. \
                Defaults to None.
            cls (type, optional): current class. Defaults to None.

        Returns:
            dict[str, type]
        """
        if current is None:
            current = dict()
        if annotations is None:
            annotations = self.__annotations__
        if cls is None:
            cls = self.__class__

        current.update(self._extractAnnotations(annotations))
        for p in cls.__bases__:
            if issubclass(p, Dataclass) and p is not Dataclass:
                current = self._loadAnnotationsIterative(current, p.__annotations__, p)

        return current

    def _extractAnnotations(self, annotations: dict[str, type]) -> dict[str, type]:
        current = dict()
        for k, v in annotations.items():
            if isinstance(v, str):
                continue

            if k in current:
                continue

            if v is Any:
                current[k] = (Any,)
            elif isinstance(v, types.UnionType):
                current[k] = tuple(t for t in v.__args__)
            else:
                current[k] = (v,)

        return current

    @property
    def __clean_dict__(self) -> dict:
        """Return a dictionary with all the attributes of the object, \
            except for the ones starting with an underscore (private).

        Returns:
            dict
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def _importDecorator(f, *_, **__) -> None:
        """Import the correct serializer for the function.

        The serializer will be put in the `_serializer` attribute of the object.
        It's mandatory to have all the functions decorated with this decorator
        to contain the name of the serializer in their name.

        Unittest will require all the serializers to be installed.

        Args:
            f (function): function to decorate

        Raises:
            ImportError: Could not import the correct serializer
        """
        libs = {
            "json": ujson,  # could be ujson but json is in the stdlib
            "yaml": yaml,  # not in the stdlib
            "toml": toml,  # not in the stdlib
        }
        serializer = None

        for k, v in libs.items():
            if k in f.__name__:
                serializer = v
                break

        def wrapper(self: Dataclass, *args, **kwargs):
            self._serializer = serializer
            return f(self, *args, **kwargs)

        return wrapper

    @property
    def to_dict(self) -> dict:
        """Return a dictionary with all the attributes of the object.

        Returns:
            dict
        """

        def iterable_type(var: any) -> type:
            if isinstance(var, (list, tuple, set)):
                return var.__class__

            return None

        d = {}

        for k, v in self.__clean_dict__.items():
            if t := iterable_type(v):
                # handle recursive lists
                d[k] = t(i.to_dict if isinstance(i, Dataclass) else i for i in v)
            elif isinstance(v, Dataclass):
                # handle recursive dataclasses
                d[k] = v.to_dict
            else:
                # simple types
                d[k] = v

        return d

    @property
    def frozen(self) -> bool:
        """Return the frozen status of the object."""
        return self._frozen

    @property
    @_importDecorator
    def to_json(self) -> str:
        """
        Return a json representation of the object.

        Attributes are recursively converted to json.

        Returns:
            str
        """
        dict_data = self.to_dict

        # all the sets and tuples are converted to lists
        # because json doesn't support them
        for k, v in dict_data.items():
            if isinstance(v, (set, tuple)):
                dict_data[k] = list(v)

        return self._serializer.dumps(dict_data)

    @property
    def to_json_pretty(self) -> str:
        """Return a pretty json representation of the object.

        Returns:
            str
        """
        return self._serializer.dumps(self._serializer.loads(self.to_json), indent=4)

    @property
    @_importDecorator
    def to_toml(self) -> str:
        """Return a toml representation of the object.

        Returns:
            str
        """
        return self._serializer.dumps(self.to_dict)

    @property
    @_importDecorator
    def to_yaml(self) -> str:
        """Return a yaml representation of the object.

        Returns:
            str
        """
        return self._serializer.dump(self.to_dict)

    @property
    def attributes(self) -> list:
        """Return a list of all the attributes of the class.

        Returns:
            list
        """
        return list(self.__class_attributes__.keys())

    @classmethod
    @_importDecorator
    def from_json(cls, json_string: str) -> Dataclass:
        """Create an object from a json string.

        Args:
            json_string (str): json string

        Returns:
            Dataclass
        """
        cls._deserialized = True
        return cls(**cls._serializer.loads(json_string))

    @classmethod
    @_importDecorator
    def from_toml(cls, toml_string: str) -> Dataclass:
        """Create an object from a toml string.

        Args:
            toml_string (str): toml string

        Returns:
            Dataclass
        """
        cls._deserialized = True
        return cls(**cls._serializer.loads(toml_string))

    @classmethod
    @_importDecorator
    def from_yaml(cls, yaml_string: str) -> Dataclass:
        """Create an object from a yaml string.

        Args:
            yaml_string (str): yaml string

        Returns:
            Dataclass
        """
        cls._deserialized = True
        return cls(
            **cls._serializer.load(yaml_string, Loader=cls._serializer.FullLoader)
        )

    @classmethod
    def from_dict(cls, d: dict) -> Dataclass:
        """Create an object from a dictionary.

        Args:
            d (dict): dictionary

        Returns:
            Dataclass
        """
        cls._deserialized = True
        return cls(**d)
