const bookedFilmedStorage = document.querySelector('#corf');


export function corfMoviesHandler() {
    const filmsListContainer = document.querySelector('#corf-films ul')

    bookedFilmedStorage.addEventListener('click', (event) => {
        let lsKeys = Object.keys(localStorage);
        let lsValues = [];
        let filmIfo;



        for (let key of lsKeys) {
            if (isNaN(key)) {
                continue;
            }

            filmIfo = (JSON.parse(localStorage.getItem(key)));


        }
        console.log(lsValues)

    })
}