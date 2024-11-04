from pydantic import BaseModel, Field, field_serializer, AliasPath, AliasChoices
from typing import List, Optional, Dict, Any
import pendulum
from icecream import ic


class RateMovieRequestModel(BaseModel):
    film: int
    user: int
    rating: int
    text: str = ''

