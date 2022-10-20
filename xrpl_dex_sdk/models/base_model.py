from dataclasses import dataclass, fields
from enum import Enum
import json
from typing import (
    Any,
    Dict,
    List,
    Type,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)
from .required import REQUIRED


@dataclass(frozen=True)
class BaseModel:
    @classmethod
    def is_dict_of_model(cls: Type["BaseModel"], dictionary: Any) -> bool:
        """
        Checks whether the provided ``dictionary`` is a dictionary representation
        of this class.

        **Note:** This only checks the exact model, and does not count model
        inheritance. This method returns ``False`` if the dictionary represents
        a subclass of this class.

        Args:
            dictionary: The dictionary to check.

        Returns:
            True if dictionary is a ``dict`` representation of an instance of this
            class; False if not.
        """
        return (
            isinstance(dictionary, dict)
            and set(get_type_hints(cls).keys()).issuperset(set(dictionary.keys()))
            and all(
                [
                    attr in dictionary
                    for attr, value in get_type_hints(cls).items()
                    if value is REQUIRED
                ]
            )
        )

    @classmethod
    def from_dict(cls, values: Dict[str, Any]):
        class_types = get_type_hints(cls)

        args = {}
        for param in values:
            if param not in class_types:
                raise Exception(f"{param} not a valid parameter for {cls.__name__}")

            args[param] = cls._from_dict_single_param(param, class_types[param], values[param])

        init = cls._get_only_init_args(args)
        return cls(**init)

    @classmethod
    def _from_dict_single_param(
        cls: Type["BaseModel"],
        param: str,
        param_type: Type[Any],
        param_value: Union[int, str, bool, "BaseModel", Enum, List[Any], Dict[str, Any]],
    ) -> Any:
        """Recursively handles each individual param in `from_dict`."""
        param_type_origin = get_origin(param_type)
        # returns `list` if a List, `Union` if a Union, None otherwise

        if param_type_origin is list and isinstance(param_value, list):
            # expected a List, received a List
            list_type = get_args(param_type)[0]
            return [cls._from_dict_single_param(param, list_type, item) for item in param_value]

        if param_type_origin is Union:
            for param_type_option in get_args(param_type):
                # iterate through the types Union-ed together
                try:
                    # try to use this Union-ed type to process param_value
                    return cls._from_dict_single_param(param, param_type_option, param_value)
                except Exception:
                    # this Union-ed type did not work, move onto the next one
                    pass

        # no more collections (no params expect a Dict)

        if param_type is Any:
            # param_type is Any (e.g. will accept anything)
            return param_value

        if isinstance(param_type, type) and isinstance(param_value, param_type):
            # expected an object, received the correct object
            return param_value

        if (
            isinstance(param_type, type)
            and issubclass(param_type, Enum)
            and param_value in list(param_type)
        ):
            # expected an Enum and received a valid value for it.
            # for some reason required for string enums.
            return param_value

        if (
            isinstance(param_type, type)
            and issubclass(param_type, Enum)
            and isinstance(param_value, str)
        ):
            if not getattr(param_type, param_value):
                error_message = f"Cannot cast {param_value} to type {param_type} for {param}"
            else:
                return getattr(param_type, param_value)

        if (
            isinstance(param_type, type)
            and issubclass(param_type, BaseModel)
            and isinstance(param_value, dict)
        ):
            # expected an XRPL Model, received a Dict
            return cast(BaseModel, param_type).from_dict(param_value)

        # received something we didn't expect, raise an error
        if isinstance(param_type, type) and issubclass(param_type, BaseModel):
            error_message = (
                f"{param} expected a {param_type} or a Dict representing {param_type}, "
                f"received a {type(param_value)}"
            )
        else:
            error_message = f"{param} expected a {param_type}, received a {type(param_value)}"
        raise Exception(error_message)

    @classmethod
    def _get_only_init_args(cls: Type["BaseModel"], args: Dict[str, Any]) -> Dict[str, Any]:
        init_keys = {field.name for field in fields(cls) if field.init is True}
        valid_args = {key: value for key, value in args.items() if key in init_keys}
        return valid_args

    def __post_init__(self: "BaseModel") -> None:
        """Called by dataclasses immediately after __init__."""
        self.validate()

    def validate(self: "BaseModel") -> None:
        """
        Raises if this object is invalid.

        Raises:
            Exception: if this object is invalid.
        """
        errors = self._get_errors()
        if len(errors) > 0:
            raise Exception(str(errors))

    def is_valid(self: "BaseModel") -> bool:
        """
        Returns whether this BaseModel is valid.

        Returns:
            Whether this BaseModel is valid.
        """
        return len(self._get_errors()) == 0

    def _get_errors(self: "BaseModel") -> Dict[str, str]:
        """
        Extended in subclasses to define custom validation logic.

        Returns:
            Dictionary of any errors found on self.
        """
        return {
            attr: f"{attr} is not set" for attr, value in self.__dict__.items() if value is REQUIRED
        }

    def to_dict(self: "BaseModel") -> Dict[str, Any]:
        """
        Returns the dictionary representation of a BaseModel.

        If not overridden, returns the object dict with all non-None values.

        Returns:
            The dictionary representation of a BaseModel.
        """
        # mypy doesn't realize that BaseModel has a field called __dataclass_fields__
        dataclass_fields = self.__dataclass_fields__.keys()  # type: ignore
        return {
            key: self._to_dict_elem(getattr(self, key))
            for key in dataclass_fields
            if getattr(self, key) is not None
        }

    def to_json(self: "BaseModel") -> str:
        """
        Returns a JSON string representation of a BaseModel.

        If not overridden, returns the object dict with all non-None values.

        Returns:
            JSON string representation of a BaseModel.
        """
        return json.dumps(self.to_dict())

    def _to_dict_elem(self: "BaseModel", elem: Any) -> Any:
        if isinstance(elem, BaseModel):
            return elem.to_dict()
        if isinstance(elem, Enum):
            return elem.value
        if isinstance(elem, list):
            return [self._to_dict_elem(sub_elem) for sub_elem in elem if sub_elem is not None]
        return elem

    def __eq__(self: "BaseModel", other: object) -> bool:
        """Compares a BaseModel to another object to determine if they are equal."""
        return isinstance(other, "BaseModel") and self.to_dict() == other.to_dict()

    def __repr__(self: "BaseModel") -> str:
        """Returns a string representation of a BaseModel object"""
        repr_items = [f"{key}={repr(value)}" for key, value in self.to_dict().items()]
        return f"{type(self).__name__}({repr_items})"
