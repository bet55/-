import {fetchMovies} from "./movie/movies_fetching.js";
import {showMovieHandler} from "./movie/movie_information.js";
// import {settingUserHandler} from "./movie/set_user.js";
// import {showRatingNotesHandler} from "./movie/rating_toggler.js";
// import {selectOptionHandler} from "./movie/movie_options.js";
// import {corfMoviesHandler} from "./utils/movies_corf.js";
// import {showScrollButtonHandler} from "./utils/scroll_up_button.js";



fetchMovies().then(movies => {
    const allMovies = movies;

    // settingUserHandler() // выбор пользователя
    // showRatingNotesHandler() // отображения оценок
    showMovieHandler(allMovies); // отрисовки большого постера
    // selectOptionHandler(allMovies) // применение действия к фильму
    // corfMoviesHandler() // корзина с выбранными фильмами
    // showScrollButtonHandler() // кнопка скролла наверх

}).catch(e => {
    console.log(e)
})


