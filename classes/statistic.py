from lists.models import Film
import pandas as pd
import plotly
import plotly.express as px


class Statistic:

    @classmethod
    def get_movies_statistic(cls):
        film_model = Film.mgr.filter(is_archive=True).values()
        df = pd.DataFrame(film_model)
        stats = {
            'total_duration': df['duration'].sum(),
            'rating_kp': round(df['rating_kp'].mean(), 2),
            'rating_imdb': round(df['rating_imdb'].mean(), 2),
            'count': len(df),
        }

        return stats

    def most_popular_actor(self):
        pass

    @classmethod
    def draw(cls):
        film_model = Film.mgr.filter(is_archive=True).values()
        df = pd.DataFrame(film_model)
        figure_config = {
            'x': 'rating_kp',
            'width': 800,
            'color_discrete_sequence': ['#9bab6e'],
            'labels': {'rating_kp': 'Средняя оценка пользователей', 'count': 'Количество оценок'},
        }
        figure = px.histogram(df, **figure_config)
        graph_div = plotly.offline.plot(figure, auto_open=False, output_type="div")

        return graph_div
