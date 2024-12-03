const rateToggler = document.querySelector('#rate-toggle');

const changeNotesVisibility = () => {
    let visibility = 'hidden';

    return () => {

        const rateNotes = document.querySelectorAll('.note-container')
        visibility = visibility === 'visible' ? 'hidden' : 'visible';

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
        console.log('show notes!');
        visibilityToggler();
    })

}
