import {fetchMovies} from "./movie/fetching.js";
import {fillMovieCard} from "./movie/card_filling.js";
import {selectOptionHandler} from "./movie/select_options.js";
// import {showRatingNotesHandler} from "./movie/rating_toggler.js";


fetchMovies().then(movies => {
    const allMovies = movies;

    // showRatingNotesHandler() // отображения оценок
    fillMovieCard(allMovies); // отрисовки большого постера
    // selectOptionHandler(allMovies) // применение опции к фильму

}).catch(e => {
    console.error(e)
})


