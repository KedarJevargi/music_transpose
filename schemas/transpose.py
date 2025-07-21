from pydantic import BaseModel, Field
from typing import Annotated, Optional
from pydantic import model_validator


class TransposeRequest(BaseModel):
    user_id: Annotated[str, Field(...)]
    notes: Annotated[str, Field(...)]
    mode: Annotated[str, Field(...)]
    semitones: Annotated[Optional[int], Field(default=None)]
    from_scale: Annotated[Optional[str], Field(default=None)]
    to_scale: Annotated[Optional[str], Field(default=None)]

    @model_validator(mode='after')
    def check_conditional_fields(self):
        if self.mode == "semitone" and self.semitones is None:
            raise ValueError("semitones is required when mode is 'semitone'")
        if self.mode == "scale" and (self.from_scale is None or self.to_scale is None):
            raise ValueError("from_scale and to_scale are required when mode is 'scale'")
        return self
