from abc import ABC
from dataclasses import field
from pydantic.dataclasses import dataclass

import yaml

from .printing import print_nested_dict


@dataclass(config=dict(validate_assignment=True))
class Settings(ABC):
    config_dict: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.config_dict:
            return

        for field_name, field_value in self.__annotations__.items():
            if field_name not in self.config_dict:
                continue

            if issubclass(field_value, Settings):
                setattr(self, field_name, field_value(config_dict=self.config_dict[field_name]))
            else:
                setattr(self, field_name, self.config_dict[field_name])

    @classmethod
    def from_yaml(cls, file_path: str, encoding: str = "utf-8") -> "Settings":
        with open(file_path, "r", encoding=encoding) as file:
            yaml_data = yaml.safe_load(file)

        return cls(config_dict=yaml_data or {})

    def to_dict(self) -> dict:
        output_dict = {}

        for field_name, field_value in self.__annotations__.items():
            if issubclass(field_value, Settings):
                output_dict[field_name] = getattr(self, field_name).to_dict()
            else:
                output_dict[field_name] = getattr(self, field_name)

        return output_dict

    def to_yaml(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            yaml.dump(self.to_dict(), file, default_flow_style=False)

    def print(self) -> None:
        print_nested_dict(self.to_dict())
