import {formatTime} from "../utils/format_time.js";

const moviePosters = document.querySelector('.posters-grid')

const cardImg = document.querySelector('.card-img')
const cardTitle = document.querySelector('.card-title')
const cardDescription = document.querySelector('.card-description')
const cardRealiseDate = document.querySelector('.card-realise')
const cardDuration = document.querySelector('.card-duration')
const cardLink = document.querySelector('.card-link a')


const showMoviePoster = (movieId, allMovies) => {

    cardImg.src = allMovies[movieId].poster;
    cardImg.style.visibility = 'visible';
    cardTitle.textContent = allMovies[movieId].name;
    cardDescription.textContent = allMovies[movieId].description;
    cardRealiseDate.textContent = allMovies[movieId].premiere;
    cardDuration.textContent = formatTime(allMovies[movieId].duration);
    cardLink.textContent = `https://www.kinopoisk.ru/film/${allMovies[movieId].kp_id}/`
    cardLink.href = `https://www.kinopoisk.ru/film/${allMovies[movieId].kp_id}/`
}

export function fillMovieCard(allMovies) {

    moviePosters.addEventListener('click', async (event) => {
        const target = event.target;
        const classList = target.classList;

        // Проверяем, что нажали на постер или один из перекрывающих элементов
        const isPosterClicked =
            classList.contains('poster-container') ||
            classList.contains('poster-img') ||
            classList.contains('note-container');

        if (isPosterClicked) {
            const movieId = target.dataset.kpId;

            showMoviePoster(movieId, allMovies);
        }

    })

}