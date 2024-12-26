import {formatTime} from "../utils/format_time.js";

const moviePosters = document.querySelector('.posters-grid')

const cardImg = document.querySelector('.card-img')
const cardTitle = document.querySelector('.card-title')
const cardDescription = document.querySelector('.card-description')
const cardRealiseDate = document.querySelector('.card-realise')
const cardDuration = document.querySelector('.card-duration')
const cardLink = document.querySelector('.card-link a')


const showMoviePoster = (movieInfo) => {

    cardImg.src = movieInfo.poster;
    cardImg.style.visibility = 'visible';
    cardTitle.textContent = movieInfo.name;
    cardDescription.textContent = movieInfo.description;
    cardRealiseDate.textContent = movieInfo.premiere;
    cardDuration.textContent = formatTime(movieInfo.duration);
    cardLink.textContent = `https://www.kinopoisk.ru/film/${movieInfo.kp_id}/`
    cardLink.href = `https://www.kinopoisk.ru/film/${movieInfo.kp_id}/`


}

export function fillMovieCard(allMovies) {

    console.log(allMovies)

    // Возможность раскрывать/прятать текст описания
    cardDescription.addEventListener('click', e => {

        if (cardDescription.classList.contains('card-description-hidden')) {
            cardDescription.classList.remove('card-description-hidden');
        } else {
            cardDescription.classList.add('card-description-hidden');
        }

    })

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
            const movieInfo = allMovies[movieId];
            showMoviePoster(movieInfo);
        }

    })

}