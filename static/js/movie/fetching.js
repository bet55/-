

export const fetchMovies = async () => {
    const getMoviesUrl = `${document.URL}?format=json`.replace('#', '');

    const response = await fetch(getMoviesUrl);

    if (!response.ok) {
        const message = `Movies request error: ${response.status}`;
        console.error(message);
    }
    return await response.json();
}

