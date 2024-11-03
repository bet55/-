import {getCookie, setCookie, deleteCookie} from "./cookie.js";

const rateToggler = document.querySelector('.btn-rate-toggle');

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
    const optionsList = document.querySelector(`.options-list[data-kp-id="${movieId}"]`);
    const isVisible = optionsList.style.visibility;
    optionsList.style.visibility = isVisible === "visible" ? "hidden" : "visible";
}


const rateMovie = (target) => {

    const showRateNoteForm = () => {
        openModal()
    }

    const rateRequest = () => {
        const rateUrl = 'http://localhost:8000/movies/rate';
        const sendData = {
            user_id: 1,
            movie_id: 1,
            rating: 1,
            message: 1,
        }
        fetch(rateUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sendData)
        }).then((rs) => rs.json()).then((data) => {
            console.log(data)
        });

    }
    const createNoteElement = (movieId) => {
        const noteContainer = document.querySelector(`.poster-container[data-kp-id="${movieId}"] .note-container`)
        const noteDiv = document.createElement('div')
        const noteH2 = document.createElement('h2')
        const noteP = document.createElement('p')


        noteP.textContent = 'Оценка?'
        noteH2.textContent = 'Комментарий'
        noteDiv.append(noteH2, noteP)
        noteDiv.classList.add('note')

        noteContainer.append(noteDiv)
    }

    const movieId = target.parentNode.dataset.kpId;
    const user = getCookie('user')
    if (!user) {
        alert('Выберите пользователя')
        return false
    }

    showRateNoteForm()
    // rateRequest()


    return true

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
    const user = usersSelector.value;
    setCookie('user', user)

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

function changeNotesVisibility() {
    let visibility = 'visible';

    return () => {
        const rateNotes = document.querySelectorAll('.note-container')
        visibility = visibility === 'visible' ? 'hidden' : 'visible';

        rateNotes.forEach(note => {
            note.style.visibility = visibility
        })
    }
}

const rateNotesToggler = changeNotesVisibility()

rateToggler.addEventListener('click', (event) => {
    rateNotesToggler();
})


const btnUp = {
    el: document.querySelector('.btn-up'),
    scrolling: false,
    show() {
        if (this.el.classList.contains('btn-hide') && !this.el.classList.contains('btn-hiding')) {
            this.el.classList.remove('btn-hide');
            this.el.classList.add('btn-hiding');
            window.setTimeout(() => {
                this.el.classList.remove('btn-hiding');
            }, 300);
        }
    },
    hide() {
        if (!this.el.classList.contains('btn-hide') && !this.el.classList.contains('btn-hiding')) {
            this.el.classList.add('btn-hiding');
            window.setTimeout(() => {
                this.el.classList.add('btn-hide');
                this.el.classList.remove('btn-hiding');
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

let focusedElementBeforeModal;
const modal = document.getElementById('modal');
const modalOverlay = document.querySelector('.modal-overlay');

const openModal = () => {
  // Save current focus
  focusedElementBeforeModal = document.activeElement;

  // Listen for and trap the keyboard
  modal.addEventListener('keydown', trapTabKey);

  // Listen for indicators to close the modal
  modalOverlay.addEventListener('click', closeModal);
  // Close btn
  const closeBtn = document.querySelector('.close-btn');
  closeBtn.addEventListener('click', closeModal);

  // submit form
  const form = document.getElementById('review-form');
  form.addEventListener('submit', submitAddReview, false);

  // Find all focusable children
  var focusableElementsString = 'a[href], area[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), iframe, object, embed, [tabindex="0"], [contenteditable]';
  var focusableElements = modal.querySelectorAll(focusableElementsString);
  // Convert NodeList to Array
  focusableElements = Array.prototype.slice.call(focusableElements);

  var firstTabStop = focusableElements[0];
  var lastTabStop = focusableElements[focusableElements.length - 1];

  // Show the modal and overlay
  modal.classList.add('show');
  modalOverlay.classList.add('show');

  // Focus first child
  // firstTabStop.focus();
  const reviewName = document.getElementById('reviewName');
  reviewName.focus();

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
      closeModal();
    }
  }
};

const submitAddReview = (e) => {
  // console.log(e);
  console.log('Form subbmitted!');
  e.preventDefault();
  closeModal();
};

const closeModal = () => {
  // Hide the modal and overlay
  modal.classList.remove('show');
  modalOverlay.classList.remove('show');

  const form = document.getElementById('review-form');
  form.reset();
  // Set focus back to element that had it before the modal was opened
  focusedElementBeforeModal.focus();
};

const setFocus = (evt) => {
  const rateRadios = document.getElementsByName('rate');
  const rateRadiosArr = Array.from(rateRadios);
  const anyChecked = rateRadiosArr.some(radio => { return radio.checked === true; });
  // console.log('anyChecked', anyChecked);
  if (!anyChecked) {
    const star1 = document.getElementById('star1');
    star1.focus();
    // star1.checked = true;
  }
};

const navRadioGroup = (evt) => {
  // console.log('key', evt.key, 'code', evt.code, 'which', evt.which);
  // console.log(evt);

  const star1 = document.getElementById('star1');
  const star2 = document.getElementById('star2');
  const star3 = document.getElementById('star3');
  const star4 = document.getElementById('star4');
  const star5 = document.getElementById('star5');

  if (['ArrowRight', 'ArrowLeft', 'ArrowDown', 'ArrowUp'].includes(evt.key)) {
    evt.preventDefault();
    // console.log('attempting return');
    if (evt.key === 'ArrowRight' || evt.key === 'ArrowDown') {
      switch(evt.target.id) {
        case 'star1':
          star2.focus();
          star2.checked = true;
          break;
        case 'star2':
          star3.focus();
          star3.checked = true;
          break;
        case 'star3':
          star4.focus();
          star4.checked = true;
          break;
        case 'star4':
          star5.focus();
          star5.checked = true;
          break;
        case 'star5':
          star1.focus();
          star1.checked = true;
          break;
      }
    } else if (evt.key === 'ArrowLeft' || evt.key === 'ArrowUp') {
      switch(evt.target.id) {
        case 'star1':
          star5.focus();
          star5.checked = true;
          break;
        case 'star2':
          star1.focus();
          star1.checked = true;
          break;
        case 'star3':
          star2.focus();
          star2.checked = true;
          break;
        case 'star4':
          star3.focus();
          star3.checked = true;
          break;
        case 'star5':
          star4.focus();
          star4.checked = true;
          break;
      }
    }
  }
};