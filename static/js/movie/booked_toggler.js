export const bookedToggle = (movieId, unbook = false) => {
    const unBookedImg = 'bm_grey';
    const bookedImg = 'bm_gold';

    const bookedBtn = document.querySelector(`.options-list[data-kp-id="${movieId}"] .btn-bookmark img`);

    if (!Boolean(bookedBtn)) {
        return false;
    }

    if (unbook) {
        bookedBtn.classList.remove('booked');
        bookedBtn.src = bookedBtn.src.replace(bookedImg, unBookedImg)
    } else {
        bookedBtn.classList.add('booked');
        bookedBtn.src = bookedBtn.src.replace(unBookedImg, bookedImg)
    }
}