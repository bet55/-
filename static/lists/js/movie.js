const moviePosters = document.querySelector('.movie-posters')

const cardImg = document.querySelector('.movie-card img')
const cardTitle = document.querySelector('.movie-card h2')
const cardDescription = document.querySelector('.movie-card p')
const cardRealiseDate = document.querySelector('.movie-card h3')
const cardDuration = document.querySelector('.movie-card p:last-child')

const getMoviesUrl = document.URL + '?format=json'

const getTimeFromMins = (mins) => {
    let hours = Math.trunc(mins/60);
    let minutes = mins % 60;
    return hours + ':' + minutes;
}


const fetchMovies = async (url) => {
    const response = await fetch(url);

    if (!response.ok) {
        const message = `Movies request error: ${response.status}`;
        console.log(message);
    }
    const moviesList = await response.json();
    const moviesJson = {};
    moviesList.forEach((e) => {
            moviesJson[e.kp_id] = e
    })
    return moviesJson;
}


let allMovies;
fetchMovies(getMoviesUrl).then(movies => allMovies = movies)


moviePosters.addEventListener('mouseover', async (event) => {
    let target = event.target;
    let movieId = target.dataset.kpId;

    if (target.classList.contains('poster')) {

        cardImg.src = target.src;
        cardTitle.textContent = allMovies[movieId].name;
        cardDescription.textContent = allMovies[movieId].description;
        cardRealiseDate.textContent = allMovies[movieId].premiere;
        cardDuration.textContent = getTimeFromMins(allMovies[movieId].duration);

    }
})