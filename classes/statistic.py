from lists.models import Film
import pandas as pd


class Statistic:
    def total_watch_hours(self):
        film_model = Film.mgr.filter(is_archive=True).values()
        df = pd.DataFrame(film_model)
        stats = {
            'total_duration': df['duration'].sum(),
            'rating_kp': df['rating_kp'].mean(),
            'rating_imdb': df['rating_imdb'].mean(),
            'count': len(df),
        }

        return stats

    def most_popular_actor(self):
        pass
