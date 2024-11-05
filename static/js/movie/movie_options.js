import {getCookie} from "../utils/cookie.js";
import {openModal} from "./rating_modal.js";

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
    }
    else {
        openModal(movieId);
    }

}

const addMovieToBookmark = (target, allMovies) => {
    const unBookedImg = 'bm_grey';
    const bookedImg = 'bm_gold';
    const movieId = target.parentNode.dataset.kpId;

    const btnImg = target.querySelector('img');
    const imgSrc = btnImg.src;
    if (imgSrc.includes(bookedImg)) {
        btnImg.src = imgSrc.replace(bookedImg, unBookedImg);
        localStorage.removeItem(movieId);
    } else {
        btnImg.src = imgSrc.replace(unBookedImg, bookedImg);


        console.log(movieId, allMovies[movieId])
        localStorage.setItem(movieId, JSON.stringify(allMovies[movieId]));
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

