from __future__ import annotations

import json
import typing
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

if TYPE_CHECKING:
    from typing import Any
    from typing import Union


def generate_type(depth: int) -> str:
    if depth <= 0:
        return ''
    return f"""ofType {{ name kind {generate_type(depth - 1)} }}"""


def generate_schema_request(depth: int) -> str:
    request = f"""{{
  __schema {{
    queryType {{
      name
    }}
    subscriptionType {{
      name
    }}
    mutationType {{
      name
    }}
    types {{
      kind
      name
      {generate_type(depth)}
      fields {{
        name
        args {{
          name
          type {{
            name
            kind
            {generate_type(depth)}
          }}
        }}
        type {{
          name
          kind
          {generate_type(depth)}
        }}
      }}
      inputFields {{
        name
        type {{
          kind
          name
          {generate_type(depth)}
        }}
      }}
      interfaces {{
        name
        kind
        {generate_type(depth)}
      }}
      enumValues {{
        name
      }}
    }}
  }}
}}
"""
    return request


class ENUM(str, Enum):
    ...


class GraphQLType(ENUM):
    STRING = 'String'
    INT = 'Int'
    BOOLEAN = 'Boolean'
    FLOAT = 'Float'
    ID = 'ID'


class Subscription(BaseModel):
    ...

    model_config = ConfigDict(
        extra='forbid'
    )


class Interface(BaseModel):
    ...

    model_config = ConfigDict(
        extra='forbid'
    )


class Payload(BaseModel):
    typename: bool = Field(default=False, alias='__typename')

    model_config = ConfigDict(
        extra='forbid',
        strict=True
    )

    def dict_to_custom_string(self, any_object: Any) -> str:
        pairs = []
        match any_object:
            case list():
                for item in any_object:
                    pairs.append(self.dict_to_custom_string(item))
            case dict():
                for key, value in any_object.items():
                    match value:
                        case Payload():
                            pairs.append(f'{key} {{ {value.render()} }}')
                        case dict():
                            pairs.append(f'{key} {{ {self.dict_to_custom_string(value)} }}')
                        case list():
                            for item in any_object:
                                pairs.append(self.dict_to_custom_string(item))
                        case _:
                            if value is True:
                                pairs.append(f'{key}')
        return ' '.join(pairs)

    def render(self) -> str:
        return self.dict_to_custom_string(self.model_dump(exclude_none=True, by_alias=True))


class Input(BaseModel):

    model_config = ConfigDict(
        extra='forbid',
        strict=True
    )

    @staticmethod
    def _parse_enum(value: Enum) -> str:
        return f'{value.name}'

    @staticmethod
    def _parse_bool(value: bool) -> str:
        return f'{str(value).lower()}'

    @staticmethod
    def _parse_num(value: int | float) -> str:
        return f'{value}'

    @staticmethod
    def _parse_str(value: Any) -> str:
        try:
            return json.dumps(json.loads(json.dumps(value)))
        except ValueError:
            return f'"{value}"'

    @staticmethod
    def _parse_tuple(value: tuple[Any, ...]) -> str:
        return f'{", ".join(map(str, value))}'

    def parse_inputs(self, value: Any) -> str:
        match value:
            case Enum():
                response = f'{self._parse_enum(value)}'
            case bool():
                response = f'{self._parse_bool(value)}'
            case int() | float():
                response = f'{self._parse_num(value)}'
            case tuple():
                response = f'{self._parse_tuple(value)}'
            case list():
                values = []
                for item in value:
                    values.append(self.parse_inputs(item))
                response = f'[{", ".join(values)}]'
            case dict():
                pairs = []
                for key, values in value.items():
                    pairs.append(f'{key}: {self.parse_inputs(values)}')
                response = ', '.join(pairs)
            case _:
                response = f'{self._parse_str(value)}'
        return response

    def dict_to_custom_string(self, any_object: Any) -> str:
        pairs = []
        for key, value in any_object.items():
            match value:
                case list():
                    values = []
                    for item in value:
                        values.append(self.parse_inputs(item))
                    pairs.append(f'{key}: [{", ".join(values)}]')
                case dict():
                    values = []
                    for key_nested, value_nested in value.items():
                        values.append(f'{key_nested}: {{{self.parse_inputs(value_nested)}}}')
                    pairs.append(f'{key}: {{{", ".join(values)}}}]')
                case _:
                    pairs.append(f'{key}: {self.parse_inputs(value)}')
        return ', '.join(pairs)

    def render(self) -> str:
        return self.dict_to_custom_string(self.model_dump(exclude_none=True, by_alias=True))


class Mutation(BaseModel):
    payload: Payload | bool
    _name: str

    model_config = ConfigDict(
        extra='forbid'
    )

    def dict_to_custom_string(self, value: dict[str, Any]) -> str:
        if isinstance(value, Input):
            return f'{{ {value.render()} }}'
        elif isinstance(value, list):
            pairs = []
            for item in value:
                pairs.append(self.dict_to_custom_string(item))
            return f"[ {', '.join(pairs)}]"
        elif isinstance(value, dict):
            pairs = []
            for key, values in value.items():
                pairs.append(f'{key}: {self.dict_to_custom_string(values)}')
            return f'{{ {", ".join(pairs)} }}'
        elif isinstance(value, str):
            return f'"{value}"'
        else:
            return f'{value}'

    def render(self) -> str:
        mutation_name: str = self._name
        payload: str = ''
        if isinstance(self.payload, Payload):
            payload = f'{{ {self.payload.render()} }}'

        variables: list[str] = []
        inputs = self.model_dump(exclude={'_name', 'payload'}, exclude_none=True, by_alias=True)

        for name, value in inputs.items():
            variables.append(f' {name}: {self.dict_to_custom_string(value)}')

        variable = ', '.join(variables)

        return f'mutation {{ {mutation_name} ({variable}) {payload} }}'


class Query(BaseModel):
    payload: Payload
    _name: str

    model_config = ConfigDict(
        extra='forbid'
    )

    @staticmethod
    def _parse_enum(value: Enum) -> str:
        return f'{value.name}'

    @staticmethod
    def _parse_bool(value: bool) -> str:
        return f'{str(value).lower()}'

    @staticmethod
    def _parse_num(value: int | float) -> str:
        return f'{value}'

    @staticmethod
    def _parse_str(value: Any) -> str:
        try:
            return json.dumps(json.loads(json.dumps(value)))
        except ValueError:
            return f'"{value}"'

    @staticmethod
    def _parse_tuple(value: tuple[Any, ...]) -> str:
        return f'{", ".join(map(str, value))}'

    def parse_inputs(self, value: Any) -> str:
        match value:
            case Enum():
                response = f'{self._parse_enum(value)}'
            case bool():
                response = f'{self._parse_bool(value)}'
            case int() | float():
                response = f'{self._parse_num(value)}'
            case tuple():
                response = f'{self._parse_tuple(value)}'
            case list():
                values = []
                for item in value:
                    values.append(self.parse_inputs(item))
                response = f'[ {",".join(values)} ]'
            case dict():
                pairs = []
                for key, values in value.items():
                    pairs.append(f' {{ {key}: {self.parse_inputs(values)} }} ')
                response = ', '.join(pairs)
            case _:
                response = f'{self._parse_str(value)}'
        return response

    def dict_to_custom_input(self, any_object: Any) -> str:
        pairs = []
        for key, value in any_object.items():
            match value:
                case list():
                    values = []
                    for item in value:
                        values.append(self.parse_inputs(item))
                    pairs.append(f' {key}: [ {", ".join(values)} ] ')
                case dict():
                    values = []
                    for key_nested, value_nested in value.items():
                        values.append(f'{key_nested}: {self.parse_inputs(value_nested)} ')
                    pairs.append(f'{key}: {{ { ", ".join(values) } }}')
                case _:
                    pairs.append(f'{key}: {self.parse_inputs(value)}')
        return ', '.join(pairs)

    def dict_to_custom_string(self, any_object: Any) -> str:
        pairs: list[str] = []
        match any_object:
            case list():
                for item in any_object:
                    pairs.append(self.dict_to_custom_string(item))
            case dict():
                for key, value in any_object.items():
                    match value:
                        case Payload():
                            pairs.append(f'{key} {{ {value.render()} }}')
                        case dict():
                            pairs.append(f'{key} {{ {self.dict_to_custom_string(value)} }}')
                        case list():
                            for item in any_object:
                                pairs.append(self.dict_to_custom_string(item))
                        case _:
                            if value is True:
                                pairs.append(f'{key}')
        return ' '.join(pairs)

    def render(self) -> str:
        variable: str = self.dict_to_custom_input(
            self.model_dump(exclude_none=True, exclude={'_name', 'payload'}, by_alias=True)
        )
        payload: str = self.dict_to_custom_string(self.payload.model_dump(exclude_none=True, by_alias=True))
        name: str = self._name
        if variable:
            variable = f' ( {variable} )'
        return f'{{ { name }{variable} {{ {payload} }} }}'


def concatenate_queries(queries: typing.Sequence[Union[Query, Mutation]]) -> str:
    merged_query = ''.join(query.render()[1:-1] for query in queries)
    return f'{{ {merged_query} }}'
