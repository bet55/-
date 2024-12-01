import {bookedToggle} from "../movie/booked_toggler.js";

const cart = document.querySelector('#cart');
const cartMoviesList = document.querySelector('#cart-list');

// Отрисовываем список фильмов из закладок
const createFilmsList = (filmsStorage) => {

    let filmContainer, title, poster, removeBtn;

    // Создаём новый элемент списка для каждого фильма
    filmsStorage.forEach(film => {


        title = document.createElement('span');
        poster = document.createElement('img');
        removeBtn = document.createElement('span');
        filmContainer = document.createElement('li');

        title.textContent = film['name'];
        poster.src = film['poster'];
        removeBtn.innerHTML = '&#10006';

        title.classList.add('film-title');
        removeBtn.classList.add('film-remove');

        filmContainer.dataset.kpId = film['kp_id'];
        filmContainer.append(poster, title, removeBtn);
        cartMoviesList.append(filmContainer);


        removeBtn.addEventListener('click', (e) => {
            const filmContainer = e.target.parentElement;
            const filmId = filmContainer.dataset.kpId;
            filmContainer.remove();
            localStorage.removeItem(filmId);

            // меняем картинку закладки
            bookedToggle(filmId, true);
        })

    })

}

// Получаем все элементы из стораджа, у которых ключ - это число
const getStorageFilmIds = () => {
    let lsKeys = Object.keys(localStorage);
    let lsValues = [];


    for (let key of lsKeys) {
        if (isNaN(key)) {
            continue;
        }
        lsValues.push(JSON.parse(localStorage.getItem(key)))
    }
    return lsValues;
}

// Добавляем фильм в сторадж и список закладок
const addToCart = (filmId, film) => {
    localStorage.setItem(filmId, JSON.stringify(film));

    createFilmsList([film]);
}
// Удаляем фильм из стораджа и списка закладок
const removeFromCart = (filmId) => {
    localStorage.removeItem(filmId);

    const filmContainer = document.querySelector(`li[data-kp-id="${filmId}"]`);
    filmContainer.remove();
}

// Обрабатываем кнопку показа списка фильмов из закладок
function cartMoviesHandler() {

    // Заполняем список закладок фильмами из локал стораджа
    const filmIds = getStorageFilmIds();
    createFilmsList(filmIds);

    cartMoviesList.addEventListener('click', (e) => {
        e.stopPropagation();
    })

    // Видимость списка по нажатию
    cartMoviesList.style.visibility = 'hidden' // Бредик полнейший (без этого хака нет свойства у объекта до нажатия)
    cart.addEventListener('click', (event) => {
        const visibility = (cartMoviesList.style.visibility === 'hidden') ? 'visible' : 'hidden';
        cartMoviesList.style.visibility = visibility;
    })
}

export {cartMoviesHandler, addToCart, removeFromCart}