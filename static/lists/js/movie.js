const usersSelector = document.querySelector('#users-select');

const moviePosters = document.querySelector('.movie-posters')

const cardImg = document.querySelector('.movie-card img')
const cardTitle = document.querySelector('.movie-card h2')
const cardDescription = document.querySelector('.movie-card p')
const cardRealiseDate = document.querySelector('.movie-card h3')
const cardDuration = document.querySelector('.movie-card p:last-child')

const bookedFilmedStorage = document.querySelector('#booked-films');

const getMoviesUrl = document.URL + '?format=json'

const getTimeFromMins = (mins) => {
    let hours = Math.trunc(mins / 60);
    let minutes = mins % 60;
    return `${hours} часа ${minutes} минуты`;
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
    cardImg.style.visibility = 'visible';
    cardTitle.textContent = allMovies[movieId].name;
    cardDescription.textContent = allMovies[movieId].description;
    cardRealiseDate.textContent = allMovies[movieId].premiere;
    cardDuration.textContent = getTimeFromMins(allMovies[movieId].duration);
}

const toggleMovieOptions = (target) => {
    const movieId = target.dataset.kpId;
    const optionsList = target.nextElementSibling;
    const isVisible = optionsList.style.visibility;
    optionsList.style.visibility = isVisible === "visible" ? "hidden" : "visible";
}

const rateMovie = () => {
}

const addMovieToBookmark = (target) => {
    const unBookedImg = 'bm_grey';
    const bookedImg = 'bm_gold';
    const movieId = target.parentNode.dataset.kpId;

    const btnImg = target.querySelector('img');
    const imgSrc = btnImg.src;
    if (imgSrc.includes(bookedImg)) {
        btnImg.src = imgSrc.replace(bookedImg, unBookedImg);
        localStorage.removeItem(movieId);
    } else {
        btnImg.src = imgSrc.replace(unBookedImg, bookedImg);


        console.log(movieId, allMovies[movieId])
        localStorage.setItem(movieId, JSON.stringify(allMovies[movieId]));
    }


}
const changeMovieArchiveStatus = (target) => {
    const isArchive = document.URL.includes('archive');

    const movieId = target.parentNode.dataset.kpId;
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
    const movieId = target.parentNode.dataset.kpId;
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


usersSelector.addEventListener('change', (event) => {
    // Cookie “user” does not have a proper “SameSite” attribute value. Soon, cookies without the “SameSite” attribute or with an invalid value will be treated as “Lax”. This means that the cookie will no longer be sent in third-party contexts. If your application depends on this cookie being available in such contexts, please add the “SameSite=None“ attribute to it. To know more about the “SameSite“ attribute, read https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite
    let user = usersSelector.value;
    document.cookie =  `user=${user}`;
    console.log(user);

})


moviePosters.addEventListener('click', async (event) => {
    let target = event.target;
    target = target.parentElement.classList.contains('btn-option') ? target.parentElement : target;

    if (target.classList.contains('poster')) {
        showMoviePoster(target);
        toggleMovieOptions(target);
    }

    if (target.classList.contains('btn-option')) {
        const currentBtn = target.classList[1];
        const currentFunction = optionsMap[currentBtn];
        currentFunction(target);
    }

})


bookedFilmedStorage.addEventListener('click', (event) => {
    let lsKeys = Object.keys(localStorage);
    let lsValues = [];
    for (let key of lsKeys) {
        lsValues.push(JSON.parse(localStorage.getItem(key)));
    }
    console.log(lsValues)


})


const btnUp = {
    el: document.querySelector('.btn-up'),
    scrolling: false,
    show() {
        if (this.el.classList.contains('btn-up_hide') && !this.el.classList.contains('btn-up_hiding')) {
            this.el.classList.remove('btn-up_hide');
            this.el.classList.add('btn-up_hiding');
            window.setTimeout(() => {
                this.el.classList.remove('btn-up_hiding');
            }, 300);
        }
    },
    hide() {
        if (!this.el.classList.contains('btn-up_hide') && !this.el.classList.contains('btn-up_hiding')) {
            this.el.classList.add('btn-up_hiding');
            window.setTimeout(() => {
                this.el.classList.add('btn-up_hide');
                this.el.classList.remove('btn-up_hiding');
            }, 300);
        }
    },
    addEventListener() {
        // при прокрутке окна (window)
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY || document.documentElement.scrollTop;
            if (this.scrolling && scrollY > 0) {
                return;
            }
            this.scrolling = false;
            // если пользователь прокрутил страницу более чем на 200px
            if (scrollY > 400) {
                // сделаем кнопку .btn-up видимой
                this.show();
            } else {
                // иначе скроем кнопку .btn-up
                this.hide();
            }
        });
        // при нажатии на кнопку .btn-up
        document.querySelector('.btn-up').onclick = () => {
            this.scrolling = true;
            this.hide();
            // переместиться в верхнюю часть страницы
            window.scrollTo({
                top: 0,
                left: 0,
                behavior: 'smooth'
            });
        }
    }
}

btnUp.addEventListener();