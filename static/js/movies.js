import {fetchMovies} from "./movie/movies_fetching.js";
import {settingUserHandler} from "./movie/set_user.js";
import {showRatingNotesHandler} from "./movie/rating_notes.js";
import {showMovieHandler} from "./movie/movie_information.js";
import {selectOptionHandler} from "./movie/movie_options.js";
import {corfMoviesHandler} from "./movie/movies_corf.js";
import {showScrollButtonHandler} from "./utils/scroll_up_button.js";


let allMovies;

fetchMovies().then(movies => {
    allMovies = movies

    settingUserHandler() // выбора пользователей
    showRatingNotesHandler() // отображения оценок
    showMovieHandler(allMovies) // отрисовки большого постера
    selectOptionHandler(allMovies) // применение действия к фильму
    corfMoviesHandler() // корзина с выбранными фильмами
    showScrollButtonHandler() // кнопка скролла наверх

})


