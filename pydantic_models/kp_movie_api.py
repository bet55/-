from pydantic import BaseModel, Field, field_serializer, AliasPath, AliasChoices
from typing import List, Optional, Dict, Any
import pendulum

n_url = 'https://banner2.cleanpng.com/20180715/yag/aavjmwzok.webp'

ListDict = List[Dict[str, str]]


class KpFilmGenresModel(BaseModel):
    genres: ListDict = []

    @field_serializer('genres')
    def serialize_genres(self, genres: List[dict], _info):
        return [g['name'] for g in genres if g.get('name')]


class KpFilmPersonModel(BaseModel):
    kp_id: int = Field(..., validation_alias='id')
    name: Optional[str] = ''
    photo: Optional[str] = ''


class KPFilmModel(BaseModel):
    kp_id: int = Field(..., validation_alias='id')
    name: str

    countries: ListDict = []

    budget: Optional[int] = Field(0, validation_alias=AliasChoices('', AliasPath('budget', 'value')))
    fees: Optional[int] = Field(0, validation_alias=AliasChoices('', AliasPath('fees', 'world', 'value')))
    premiere: Optional[str] = Field('1970-01-01T00:00:00.000Z', validation_alias=AliasPath('premiere', 'world'))
    description: Optional[str]
    short_description: Optional[str] = Field('...', validation_alias='shortDescription')
    slogan: Optional[str]
    duration: Optional[int] = Field(0, validation_alias='movieLength')
    poster: Optional[str] = Field(n_url, validation_alias=AliasPath('poster', 'url'))
    rating_kp: Optional[float] = Field(0.0, validation_alias=AliasPath('rating', 'kp'))
    rating_imdb: Optional[float] = Field(0.0, validation_alias=AliasPath('rating', 'imdb'))
    votes_kp: Optional[int] = Field(0, validation_alias=AliasPath('votes', 'kp'))
    votes_imdb: Optional[int] = Field(0, validation_alias=AliasPath('votes', 'imdb'))
    is_archive: bool = Field(False)

    @field_serializer('premiere')
    def serialize_premier(self, premiere: str, _info):
        return pendulum.parse(premiere).format('DD/MM/YYYY')

    @field_serializer('countries')
    def serialize_countries(self, countries: List[dict], _info):
        return [c['name'] for c in countries if c.get('name')]
