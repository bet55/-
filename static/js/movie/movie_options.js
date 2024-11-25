import {getCookie} from "../utils/cookie.js";
import {openModal} from "./rating_modal.js";
import {addToCorf, removeFromCorf} from "../utils/movies_corf.js";
import {bookedToggle} from "./booked_toggler.js";

const moviePosters = document.querySelector('.movie-posters')

const toggleMovieOptions = (target) => {
    const movieId = target.dataset.kpId;
    const optionsList = document.querySelector(`.options-list[data-kp-id="${movieId}"]`);
    const isVisible = optionsList.style.visibility;
    optionsList.style.visibility = isVisible === "visible" ? "hidden" : "visible";
}

const rateMovie = (target) => {

    const movieId = target.parentNode.dataset.kpId;
    const user = getCookie('user')

    if (!user) {
        alert('Выберите пользователя')
    } else {
        openModal(movieId);
    }

}

const paintBookedMovies = () => {

    let lsKeys = Object.keys(localStorage);

    for (let key of lsKeys) {
        if (isNaN(key)) {
            continue;
        }
        bookedToggle(key);

    }

}


const addMovieToBookmark = (target, allMovies) => {

    const movieId = target.parentNode.dataset.kpId;

    if (target.firstElementChild.classList.contains('booked')) {
        bookedToggle(movieId, true);
        removeFromCorf(movieId);


    } else {
        bookedToggle(movieId);
        addToCorf(movieId, allMovies[movieId]);
    }

}

const changeMovieArchiveStatus = (target) => {
    const isArchive = document.URL.includes('archive');

    const movieId = target.parentNode.dataset.kpId;
    const removeUrl = 'http://localhost:8000/movies/change_archive';
    const sendData = {kp_id: movieId, is_archive: !isArchive}

    fetch(removeUrl, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sendData)
    }).then((rs) => rs.json()).then((data) => {
        console.log(data)
    });

    target.parentElement.parentElement.remove();
}

const removeMovie = (target) => {
    const movieId = target.parentNode.dataset.kpId;
    const removeUrl = 'http://localhost:8000/movies/remove';
    const sendData = {kp_id: movieId}

    fetch(removeUrl, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sendData)
    }).then((rs) => rs.json()).then((data) => {
        console.log(data)
    });

    target.parentElement.parentElement.remove()
}

const optionsMap = {
    'btn-rate': rateMovie,
    'btn-bookmark': addMovieToBookmark,
    'btn-archive': changeMovieArchiveStatus,
    'btn-remove': removeMovie
}

function selectOptionHandler(allMovies) {

    paintBookedMovies();

    moviePosters.addEventListener('click', async (event) => {
        let target = event.target;
        target = target.parentElement.classList.contains('btn-option') ? target.parentElement : target;

        if (target.classList.contains('btn-option')) {

            const currentBtn = target.classList[1];
            const currentFunction = optionsMap[currentBtn];
            currentFunction(target, allMovies);
        }

    })

}


export {toggleMovieOptions, selectOptionHandler}

