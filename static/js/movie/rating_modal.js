import {createNoteElement, rateRequest} from "./rating_note.js";
import {getCookie} from "../utils/cookie.js";

const modalForm = document.querySelector('#rate-form');
const starsHint = document.querySelector('#stars-hint');
const stars = document.querySelectorAll('.rating input');
const modalOverlay = document.querySelector('#rate-modal');
const closeButton = document.querySelector('#btn-close');
const saveButton = document.querySelector('#btn-save');
const commentField = document.querySelector('#comment-area');

// Не отправляем форму
modalForm.addEventListener('submit', (e) => {
    e.preventDefault()
})

// Не пускаем нажатие под модальное окно
modalForm.addEventListener('click', (e) => {
    e.stopPropagation()
})


// Дублируем звезды числами
stars.forEach(star => {
    star.addEventListener('change', (e) => {
        const target = e.target;
        const starValue = target.value;
        starsHint.firstChild.textContent = `${starValue}/10`;
        starsHint.style.visibility = 'visible';
    })

})


// Закрываем модалку
modalOverlay.addEventListener('click', (e) => {
    const movieId = modalOverlay.dataset.kpId;
    closeModal(movieId);
})
saveButton.addEventListener('click', (e) => {
    const movieId = modalOverlay.dataset.kpId;
    closeModal(movieId, true);
})
closeButton.addEventListener('click', (e) => {
    const movieId = modalOverlay.dataset.kpId;
    closeModal(movieId);
})


const closeModal = (movieId, isSaved = false) => {

    const star = Array.from(stars).filter((star) => Boolean(star.checked) === true).pop();
    const comment = commentField.value;

    starsHint.style.visibility = 'hidden';
    modalOverlay.style.display = 'none';
    modalForm.reset();


    if (isSaved && star) {
        const rating = star.value;
        const userId = getCookie('user')

        createNoteElement(movieId, userId, rating, comment);
        rateRequest(movieId, userId, rating, comment);
    }


};

export const openModal = (movieId) => {

    modalOverlay.style.display = 'block';
    modalOverlay.dataset.kpId = movieId;

};


