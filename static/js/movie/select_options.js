import {rateMovie} from "./options/rate.js";
import {addMovieToBookmark} from "./options/book.js";
import {removeMovie} from "./options/remove.js";
import {changeMovieArchiveStatus} from "./options/archive.js";
import {bookedToggle} from "./booked_toggler.js";

const moviesGrid = document.querySelector('.posters-grid')


// Меняем иконку на активную у фильмов в закладках
const paintBookedMovies = () => {

    let lsKeys = Object.keys(localStorage);

    for (let key of lsKeys) {
        if (isNaN(key)) {
            continue;
        }
        bookedToggle(key);

    }

}

const optionsMap = {
    'opt-rate': rateMovie,
    'opt-booked': addMovieToBookmark,
    'opt-archive': changeMovieArchiveStatus,
    'opt-remove': removeMovie
}

// При нажатии на кнопку под постером фильма выбирается нужная функция
export function selectOptionHandler(allMovies) {

    paintBookedMovies();

    moviesGrid.addEventListener('click', async (event) => {
        const target = event.target;
        const posterContainer = target.parentElement.parentElement;

        if (target.classList.contains('opt')) {
            const optionName = target.classList[1];
            const currentFunction = optionsMap[optionName];
            const movieId = posterContainer.dataset.kpId;
            currentFunction(allMovies, movieId, target, posterContainer);
        }

    })

}

