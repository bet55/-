import {formatTime} from "../utils/format_time.js";
import {toggleMovieOptions} from "./movie_options.js";

const moviePosters = document.querySelector('.movie-posters')

const cardImg = document.querySelector('.card-poster')
const cardTitle = document.querySelector('.card-title')
const cardDescription = document.querySelector('.card-description')
const cardRealiseDate = document.querySelector('.card-realise')
const cardDuration = document.querySelector('.card-duration')
const cardLink = document.querySelector('.card-link a')


const showMoviePoster = (target, allMovies) => {
    let movieId = target.dataset.kpId;

    cardImg.src = allMovies[movieId].poster;
    cardImg.style.visibility = 'visible';
    cardTitle.textContent = allMovies[movieId].name;
    cardDescription.textContent = allMovies[movieId].description;
    cardRealiseDate.textContent = allMovies[movieId].premiere;
    cardDuration.textContent = formatTime(allMovies[movieId].duration);
    cardLink.textContent = `https://www.kinopoisk.ru/film/${allMovies[movieId].kp_id}/`
    cardLink.href = `https://www.kinopoisk.ru/film/${allMovies[movieId].kp_id}/`
}

export function showMovieHandler(allMovies) {
    // todo переписать на листенеры блоков с постерами
    moviePosters.addEventListener('click', async (event) => {
        let target = event.target;
        target = target.parentElement.classList.contains('btn-option') ? target.parentElement : target;

        if (target.classList.contains('poster') || target.classList.contains('note-container')) {
            showMoviePoster(target, allMovies);
            toggleMovieOptions(target);
        }

    })
//
}