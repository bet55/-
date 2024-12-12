import {createToast} from "../utils/create_toast.js";

const cartMoviesList = document.querySelector('#cart-list');

const postersGrid = document.querySelector('#posters');
const titlesContainer = document.querySelector('#invitation');


const MAX_MOVIES_COUNT = 4;
let currentMoviesCount = 0;

const addMovieToPostcard = (movieItem, movieId) => {

    // Параметры выбранного фильма
    const listImg = movieItem.querySelector('img');
    const listTitle = movieItem.querySelector('span');

    // Контейнер для постера
    const posterContainer = document.createElement('div');
    posterContainer.dataset.kpId = movieId;
    posterContainer.classList.add('poster-container');

    // Рамка постера
    const border = document.createElement('img');
    border.src = '/static/img/border/frame4.png';
    border.classList.add('border');

    // Добавляем картинку с постером
    const poster = document.createElement('img');
    poster.src = listImg.src;
    poster.dataset.kpId = movieId;
    poster.classList.add('poster');

    // Добавляем название фильма в список
    const title = document.createElement('span');
    title.dataset.kpId = movieId;
    title.innerText = listTitle.innerText;

    // Прикрепляем в открытку
    posterContainer.appendChild(border);
    posterContainer.appendChild(poster);
    postersGrid.appendChild(posterContainer);
    titlesContainer.appendChild(title);


    // Создаем обработчик удаления постеров
    posterContainer.addEventListener('click', e => {
        title.remove();
        posterContainer.remove();

        currentMoviesCount--;
    })

}


export const cartHandler = () => {


    cartMoviesList.addEventListener('click', e => {

        const movieItem = e.target.dataset.kpId ? e.target : e.target.parentNode;
        const movieId = movieItem.dataset.kpId;

        // Если уже добавили много фильмов
        if (currentMoviesCount >= MAX_MOVIES_COUNT) {
            createToast('Больше не влезет!', 'error')
            return null;
        }

        // Если такой фильм уже добавлен
        if (document.querySelector(`span[data-kp-id="${movieId}"]`)) {
            return null;
        }

        addMovieToPostcard(movieItem, movieId);
        currentMoviesCount++;


    })

}
