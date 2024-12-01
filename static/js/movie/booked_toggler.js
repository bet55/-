export const bookedToggle = (movieId, unbook = false) => {
    const unBookedImg = 'bookmark4';
    const bookedImg = 'bookmark3';

    const bookedBtn = document.querySelector(`.poster-container[data-kp-id="${movieId}"] .poster-settings .opt-booked`);

    if (!Boolean(bookedBtn)) {
        return false;
    }

    if (unbook) {
        bookedBtn.classList.remove('booked');
        bookedBtn.src = bookedBtn.src.replace(bookedImg, unBookedImg);
    } else {
        bookedBtn.classList.add('booked');
        bookedBtn.src = bookedBtn.src.replace(unBookedImg, bookedImg);
    }
}