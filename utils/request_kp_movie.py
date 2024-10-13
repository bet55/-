import httpx
from icecream import ic
from utils.get_api_token import get_api_token


base_url = 'https://api.kinopoisk.dev/v1.4/movie/'
url = '363'
headers = {'X-API-KEY': get_api_token()}
try:
    response = httpx.get(base_url + url, headers=headers)
    response.raise_for_status()
    ic(response.json())
except httpx.RequestError as exc:
    print(f"An error occurred while requesting {exc.request.url!r}.")
except httpx.HTTPStatusError as exc:
    print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

