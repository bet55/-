const bookedFilmedStorage = document.querySelector('#booked-films');


export function corfMoviesHandler() {
    bookedFilmedStorage.addEventListener('click', (event) => {
        let lsKeys = Object.keys(localStorage);
        let lsValues = [];
        for (let key of lsKeys) {
            lsValues.push(JSON.parse(localStorage.getItem(key)));
        }
        console.log(lsValues)

    })
}