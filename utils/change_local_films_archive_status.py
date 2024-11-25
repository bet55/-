import json
from icecream import ic


def change_archive_status(to_archive_movies_ids: list[int]):
    # в локальных данных о фильмах обновляем статус просмотренных фильмов

    changed_movies = []

    with open('../data/movies_to_watch_dump.json', 'r') as f:
        unwatched_movies_updated = []
        unwatched_movies = json.loads(f.read())
        for movie in unwatched_movies:
            if movie.get('id') in to_archive_movies_ids:
                changed_movies.append(movie)
            else:
                unwatched_movies_updated.append(movie)

    with open('../data/archive_movies_dump.json', 'r') as f:
        watched_movies = json.loads(f.read())
        watched_movies.extend(changed_movies)

    with open('../data/movies_to_watch_dump.json', 'w') as f:
        f.write(json.dumps(unwatched_movies_updated, indent=4, ensure_ascii=False))

    with open('../data/archive_movies_dump.json', 'w') as f:
        f.write(json.dumps(watched_movies, indent=4, ensure_ascii=False))

    return len(unwatched_movies) - len(unwatched_movies_updated)


update_moves = [840884,
                4626783,
                837525,
                5417579,
                4825582,
                5429853]

res = change_archive_status(update_moves)
ic(res)
