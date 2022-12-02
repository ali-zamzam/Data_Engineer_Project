from pydantic import BaseModel


class Prediction(BaseModel):
    review: str
