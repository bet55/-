const moviePosters = document.querySelector('.movie-posters')

const cardImg = document.querySelector('.movie-card img')
const cardTitle = document.querySelector('.movie-card h2')
const cardDescription = document.querySelector('.movie-card p')
const cardRealiseDate = document.querySelector('.movie-card h3')
const cardDuration = document.querySelector('.movie-card p:last-child')

const getMoviesUrl = document.URL + '?format=json'

const getTimeFromMins = (mins) => {
    let hours = Math.trunc(mins / 60);
    let minutes = mins % 60;
    return hours + ':' + minutes;
}

const fetchMovies = async (url) => {
    const response = await fetch(url);

    if (!response.ok) {
        const message = `Movies request error: ${response.status}`;
        console.error(message);
    }
    return await response.json();
}

let allMovies;
fetchMovies(getMoviesUrl).then(movies => allMovies = movies)

const showMoviePoster = (target) => {
    let movieId = target.dataset.kpId;

    cardImg.src = target.src;
    cardTitle.textContent = allMovies[movieId].name;
    cardDescription.textContent = allMovies[movieId].description;
    cardRealiseDate.textContent = allMovies[movieId].premiere;
    cardDuration.textContent = getTimeFromMins(allMovies[movieId].duration);
}

const toggleMovieOptions = (target) => {
    let movieId = target.dataset.kpId;
    console.log(movieId);
    let optionsList = target.nextElementSibling;
    let isVisible = optionsList.style.visibility;
    optionsList.style.visibility = isVisible === "visible" ? "hidden" : "visible";
}

const rateMovie = () => {
}

const addMovieToBookmark = (target) => {
    const unBookedImg = 'bm_grey';
    const bookedImg = 'bm_gold';

    const btnImg = target.querySelector('img');
    console.log(btnImg)
    if (btnImg.src.includes(bookedImg)) {
        console.log('in')
        btnImg.src = btnImg.src.replace(bookedImg, unBookedImg)
    } else {
        console.log('else')
        btnImg.src = btnImg.src.replace(unBookedImg, bookedImg)
    }

}
const changeMovieArchiveStatus = (target) => {
    const isArchive = document.URL.includes('archive');

    let movieId = target.parentNode.dataset.kpId;
    const removeUrl = 'http://localhost:8000/movies/change_archive';
    const sendData = {kp_id: movieId, is_archive: !isArchive}
    console.log(sendData)
    fetch(removeUrl, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sendData)
    }).then((rs) => rs.json()).then((data) => {
        console.log(data)
    });

    target.parentElement.parentElement.remove();
}

const removeMovie = (target) => {
    let movieId = target.parentNode.dataset.kpId;
    const removeUrl = 'http://localhost:8000/movies/remove';
    const sendData = {kp_id: movieId}

    fetch(removeUrl, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sendData)
    }).then((rs) => rs.json()).then((data) => {
        console.log(data)
    });

    target.parentElement.parentElement.remove()
}
const optionsMap = {
    'btn-rate': rateMovie,
    'btn-bookmark': addMovieToBookmark,
    'btn-archive': changeMovieArchiveStatus,
    'btn-remove': removeMovie
}


moviePosters.addEventListener('click', async (event) => {
    let target = event.target;

    if (target.classList.contains('poster')) {
        showMoviePoster(target);
        toggleMovieOptions(target);
    }
    console.log(target.classList)
    if (target.classList.contains('btn-option')) {
        let currentBtn = target.classList[1];
        let currentFunction = optionsMap[currentBtn];
        console.log(optionsMap[currentBtn])
        currentFunction(target);
    }

})



