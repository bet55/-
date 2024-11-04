const rateToggler = document.querySelector('.btn-rate-toggle');
const changeNotesVisibility = () => {
    let visibility = 'visible';

    return () => {
        const rateNotes = document.querySelectorAll('.note-container')
        visibility = visibility === 'visible' ? 'hidden' : 'visible';

        rateNotes.forEach(note => {
            note.style.visibility = visibility
        })
    }
}

export function showRatingNotesHandler() {
    rateToggler.addEventListener('click', (event) => {
        changeNotesVisibility();
    })


}
