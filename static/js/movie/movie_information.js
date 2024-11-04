import {formatTime} from "../utils/format_time.js";
import {toggleMovieOptions} from "./movie_options.js";

const moviePosters = document.querySelector('.movie-posters')

const cardImg = document.querySelector('.movie-card img')
const cardTitle = document.querySelector('.movie-card h2')
const cardDescription = document.querySelector('.movie-card p')
const cardRealiseDate = document.querySelector('.movie-card h3')
const cardDuration = document.querySelector('.movie-card p:last-child')


const showMoviePoster = (target, allMovies) => {
    let movieId = target.dataset.kpId;

    cardImg.src = target.src;
    cardImg.style.visibility = 'visible';
    cardTitle.textContent = allMovies[movieId].name;
    cardDescription.textContent = allMovies[movieId].description;
    cardRealiseDate.textContent = allMovies[movieId].premiere;
    cardDuration.textContent = formatTime(allMovies[movieId].duration);
}

export function showMovieHandler(allMovies) {
    // todo переписать на листенеры блоков с постерами
    moviePosters.addEventListener('click', async (event) => {
        let target = event.target;
        target = target.parentElement.classList.contains('btn-option') ? target.parentElement : target;

        if (target.classList.contains('poster')) {
            showMoviePoster(target, allMovies);
            toggleMovieOptions(target);
        }

    })

}