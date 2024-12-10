import {createToast} from "../utils/create_toast.js";

const cartMoviesList = document.querySelectorAll('#cart-list li');

const postersContainer = document.querySelector('#posters');
const titlesContainer = document.querySelector('#invitation');


const MAX_MOVIES_COUNT = 4;
let currentMoviesCount = 0;

const addMovieToPostcard = (movieItem, movieId) => {

    console.log(movieItem.dataset.kpId)
    // Параметры выбранного фильма
    const listImg = movieItem.querySelector('img');
    const listTitle = movieItem.querySelector('span');


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
    postersContainer.appendChild(poster);
    titlesContainer.appendChild(title);


    // Создаем обработчик удаления постеров
    poster.addEventListener('click', e => {
        title.remove();
        poster.remove();

        currentMoviesCount--;
    })

}


export const cartHandler = () => {
    cartMoviesList.forEach(movieItem => {

        movieItem.addEventListener('click', (e) => {
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

            addMovieToPostcard(e.target, movieId);
            currentMoviesCount++;


        })
    })
}
