const rateToggler = document.querySelector('#rate-toggle');

const changeNotesVisibility = () => {
    const rateNotes = document.querySelectorAll('.note-container')
    let visibility = localStorage.getItem('ratingVisibility') || 'hidden';

    // Сохраняем состояние со слоем оценок
    if (visibility === 'visible') {
        rateNotes.forEach(note => {
            note.style.visibility = visibility;
        })

    }


    return () => {

        visibility = (visibility === 'visible') ? 'hidden' : 'visible';

        localStorage.setItem('ratingVisibility', visibility);

        rateNotes.forEach(note => {
            note.style.visibility = visibility
        })
    }
}


const visibilityToggler = changeNotesVisibility()

export function showRatingNotesHandler() {
    if (!rateToggler) {
        return ''
    }

    rateToggler.addEventListener('click', (event) => {
        visibilityToggler();
    })

}
