const rateToggler = document.querySelector('.toggler-img');

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
let visibilityToggler = changeNotesVisibility()
export function showRatingNotesHandler() {
    rateToggler.addEventListener('click', (event) => {
        visibilityToggler();
    })


}
