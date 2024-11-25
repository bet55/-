import asyncio
import time
import httpx
import anyio
import json
from icecream import ic

from utils.movies_ids import movies_ids, archive_movies_ids
from utils.get_api_token import get_api_token

# Создаем локальный дамп фильмов с КП
async def get_movie(movie_id):
    BASE_URL = 'https://api.kinopoisk.dev/v1.4/movie/'
    headers = {'X-API-KEY': get_api_token()}

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        response = await client.get(movie_id)
        return response.json()


async def dump_movies():
    start_time = time.perf_counter()

    archive_tasks = [get_movie(mid) for mid in archive_movies_ids]
    archive_movies = await asyncio.gather(*archive_tasks)

    tasks = [get_movie(mid) for mid in movies_ids]
    movies = await asyncio.gather(*tasks)

    with open('../data/archive_movies_dump.json', 'w') as f:
        f.write(json.dumps(archive_movies, indent=4, ensure_ascii=False))

    with open('../data/movies_to_watch_dump.json', 'w') as f:
        f.write(json.dumps(movies, indent=4, ensure_ascii=False))

    end_time = time.perf_counter()
    ic(f"Запрос выполнен за: {end_time - start_time:.2f} секунд")


if __name__ == 'main':
    anyio.run(dump_movies)
