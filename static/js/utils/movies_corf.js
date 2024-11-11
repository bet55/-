import {bookedToggle} from "../movie/booked_toggler.js";

const bookedFilmedStorage = document.querySelector('#corf');
const filmsListContainer = document.querySelector('#corf-films');

const createFilmsList = (filmsStorage) => {

    const filmsList = filmsListContainer.querySelector('ul');

    let filmContainer, title, poster, removeBtn;

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
        filmsList.append(filmContainer);


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

const getStragedFilmIds = () => {
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

const addToCorf = (filmId, film) => {
    localStorage.setItem(filmId, JSON.stringify(film));

    createFilmsList([film]);
}

const removeFromCorf = (filmId) => {
    localStorage.removeItem(filmId);

    const filmContainer = document.querySelector(`li[data-kp-id="${filmId}"]`);
    filmContainer.remove();
}

function corfMoviesHandler() {

    const filmIds = getStragedFilmIds();
    createFilmsList(filmIds);

    filmsListContainer.addEventListener('click', (e) => {
        e.stopPropagation();
    })

    filmsListContainer.style.visibility = 'hidden' // Бредик полнейший
    bookedFilmedStorage.addEventListener('click', (event) => {
        const visibility = (filmsListContainer.style.visibility === 'hidden') ? 'visible' : 'hidden';
        filmsListContainer.style.visibility = visibility;
    })
}

export {corfMoviesHandler, addToCorf, removeFromCorf}