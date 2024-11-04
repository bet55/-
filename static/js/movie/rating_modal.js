let focusedElementBeforeModal;
const modal = document.getElementById('modal');
const modalOverlay = document.querySelector('.modal-overlay');

export const openModal = (movieId) => {
    const form = document.querySelector('#rate-form')
    form.style.display = 'block';

    function trapTabKey(e) {
        // Check for TAB key press
        if (e.keyCode === 9) {

            // SHIFT + TAB
            if (e.shiftKey) {
                if (document.activeElement === firstTabStop) {
                    e.preventDefault();
                    lastTabStop.focus();
                }

                // TAB
            } else {
                if (document.activeElement === lastTabStop) {
                    e.preventDefault();
                    firstTabStop.focus();
                }
            }
        }

        // ESCAPE
        if (e.keyCode === 27) {
            closeModal(movieId);
        }
    }
};

const submitAddReview = (e, movieId) => {
    // console.log(e);
    console.log('Form subbmitted!');
    e.preventDefault();
    closeModal(movieId);
};

const closeModal = (movieId, isRated = true) => {



    const stars = document.querySelectorAll('input[id^="star"]')

    const stars1 = document.querySelector('#star1')
    const stars2 = document.querySelector('#star2')
    const stars3 = document.querySelector('#star3')
    const stars4 = document.querySelector('#star4')
    const stars5 = document.querySelector('#star5')
    let starValue;

    console.log(stars1.checked,stars2.checked,stars3.checked,stars4.checked,stars5.checked)
  // console.log(stars)
    stars.forEach(e => {
        console.log(e.checked, e.value)
        if (e.checked) {
            starValue = e.value

        }
    })
    console.log(starValue, isRated, movieId)
    if (isRated && starValue) {
        createNoteElement(movieId)
    }


    // modal.classList.remove('show');
    // modalOverlay.classList.remove('show');
    //
    // const form = document.getElementById('review-form');
    // form.reset();
    //
    // focusedElementBeforeModal.focus();
};

const createNoteElement = (movieId) => {
    console.log(movieId)
    const noteContainer = document.querySelector(`.note-container[data-kp-id="${movieId}"] `)
    const noteDiv = document.createElement('div')
    const noteH2 = document.createElement('h2')
    const noteP = document.createElement('p')


    noteP.textContent = 'Оценка?'
    noteH2.textContent = '7'
    noteDiv.append(noteH2)
    noteDiv.classList.add('note')

    noteContainer.append(noteDiv)
}
