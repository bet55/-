from dataclasses import dataclass

from classes.caching import Caching
from utils import get_api_token
import httpx
from typing import ClassVar, Optional
from icecream import ic
import json


@dataclass
class KP:
    cache_duration: int = 60 * 2
    cache: Caching = Caching('kp_caching', cache_duration)
    client: ClassVar[httpx.Client] = httpx.Client
    error: str = None
    BASE_URL: ClassVar[str] = 'https://api.kinopoisk.dev/v1.4/'
    headers: ClassVar[dict] = {'X-API-KEY': get_api_token()}

    def _make_request(self, url: str, params: Optional[dict] = None) -> dict:
        with self.client(base_url=self.BASE_URL, headers=self.headers, params=params) as client:

            cache_key = f'{self.BASE_URL}{url}' + str(params)
            cache_value = self.cache.get_cache(cache_key)
            if cache_value:
                return cache_value

            try:
                response = client.get(url)
                response.raise_for_status()
                response_data = response.json()
                self.cache.set_cache(cache_key, response_data)
                return response_data
            except httpx.HTTPError as exc:
                self.error = f"HTTP Exception for {exc.request.url} - {exc}"
                ic(self.error)


@dataclass
class KP_Movie(KP):
    BASE_URL: ClassVar[str] = KP.BASE_URL + 'movie'

    def get_movie_by_id(self, movie_id: str | int) -> dict:
        movie = self._make_request(str(movie_id))
        return movie


if __name__ == 'main':
    kp = KP_Movie()
    mv = kp.get_movie_by_id(840884)

    with open('api_response_3.json', 'w') as f:
        f.write(json.dumps(mv, indent=4, ensure_ascii=False))
