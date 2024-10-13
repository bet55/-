// Получение id фильмов кинопоиска со страницы
// https://www.kinopoisk.ru/mykp/folders/4583/?format=posters&limit=50

// Из браузера
let extractMoviesIds = () => {
    const moviesBlockQuery = '#itemList .item';
    let moviesBlocks = document.querySelectorAll(moviesBlockQuery);
    let moviesIds = Array();
    moviesBlocks.forEach((li) => {
        moviesIds.push(li.id.split('_')[1]);
    })
    return moviesIds;
}

// Из приложения
let requestMoviesIds = async () => {
    const moviesUrl = 'https://www.kinopoisk.ru/user/4784402/movies/list/type/4583/sort/default/vector/desc/perpage/50/#list';
    const archiveMoviesUrl = 'https://www.kinopoisk.ru/user/4784402/movies/list/type/546990/sort/default/vector/desc/perpage/50/#list';
    const [moviesHtml, archiveMoviesHtml] = await Promise.all([
        fetch(moviesUrl),
        fetch(archiveMoviesUrl)
    ]);

    const movies = extractMoviesIds(await moviesHtml);
    const archiveMovies = extractMoviesIds(await archiveMoviesHtml);
    return {'movies': movies, 'archive_movies': archiveMovies}
}