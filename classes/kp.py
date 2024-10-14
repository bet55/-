from dataclasses import dataclass
from utils import get_api_token
import httpx
from typing import ClassVar, Optional
from icecream import ic


@dataclass
class KP:
    client: ClassVar[httpx.Client] = httpx.Client
    error: str = None
    BASE_URL: ClassVar[str] = 'https://api.kinopoisk.dev/v1.4/'
    headers: ClassVar[dict] = {'X-API-KEY': get_api_token()}

    def make_request(self, url: str, params: Optional[dict] = None) -> dict:
        with self.client(base_url=self.BASE_URL, headers=self.headers, params=params) as client:
            try:
                response = client.get(url)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as exc:
                self.error = f"HTTP Exception for {exc.request.url} - {exc}"
                ic(self.error)


@dataclass
class KP_Movie(KP):
    BASE_URL: ClassVar[str] = KP.BASE_URL + 'movie'

    def get_movie_by_id(self, movie_id: str | int) -> dict:
        movie = self.make_request(str(movie_id))
        return movie


if __name__ == 'main':
    kp = KP_Movie()
    ic(kp.get_movie_by_id(4664634))