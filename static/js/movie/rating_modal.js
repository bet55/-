import {createNoteElement, rateRequest} from "./rating_note.js";
import {getCookie} from "../utils/cookie.js";

const modalForm = document.querySelector('#rate-modal');
const ratePoster = document.querySelector('#rate-poster img');
const rateTitle = document.querySelector('.rate-title');
const starsHint = document.querySelector('#stars-hint');
const stars = document.querySelectorAll('#rate-stars input');
const closeButton = document.querySelector('#rate-modal .btn-close');
const saveButton = document.querySelector('.rate-btn-save');
// const commentField = document.querySelector('#rate-comment-area');

const userAlert = new bootstrap.Modal('#rate-modal');


// Дублируем звезды числами
stars.forEach(star => {
    star.addEventListener('change', (e) => {
        const target = e.target;
        const starValue = target.value;
        starsHint.firstChild.textContent = `${starValue}/10`;
        starsHint.style.visibility = 'visible';
    })

})


// // Закрываем модалку
saveButton.addEventListener('click', (e) => {
    const movieId = modalForm.dataset.kpId;
    closeModal(movieId, true);
})
closeButton.addEventListener('click', (e) => {
    const movieId = modalForm.dataset.kpId;
    closeModal(movieId);
})


const closeModal = (movieId, isSaved = false) => {

    const star = Array.from(stars).filter((star) => Boolean(star.checked) === true).pop();
    const comment = 'no comment';
    // const comment = commentField.value;

    starsHint.style.visibility = 'hidden';

    if (isSaved && star) {
        star.checked = false;
        const rating = star.value;
        const userId = getCookie('user');

        createNoteElement(movieId, userId, rating, comment);
        rateRequest(movieId, userId, rating, comment);
    }


};

export const showRatingModal = (movieId, allMovies) => {
    userAlert.show();
    modalForm.dataset.kpId = movieId;

    ratePoster.src = allMovies[movieId].poster;
    rateTitle.innerText = allMovies[movieId].name;
};


