// Получение id фильмов кинопоиска со страницы
// https://www.kinopoisk.ru/mykp/folders/4583/?format=posters&limit=50

// Из браузера
let extractMoviesIds = () => {
    const moviesBlockQuery = '#itemList .number';
    let moviesBlocks = document.querySelectorAll(moviesBlockQuery);
    let moviesIds = Array();
    moviesBlocks.forEach((div) => {
      moviesIds.push(div.id)
    })
    return moviesIds
}

// Из приложения
// TODO fetch