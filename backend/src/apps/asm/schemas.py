from typing import Literal, List, Dict

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class RequestSchema(BaseModel):
    """
    Request API schema.
    Converts camelCase to snake_case.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
        )
    )


class ResponseSchema(BaseModel):
    """
    Response API schema.
    Converts snake_case to camelCase.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_camel,
        )
    )


class ASMSelectionRequestSchema(RequestSchema):
    gender: Literal["male", "female"]
    age: int
    weight: float
    seizure_types: List[str]
    modifiers: List[str]


class ASMSelectionResponseSchema(ResponseSchema):
    tiers: Dict[str, List[str]]
    patient_snapshot: dict
