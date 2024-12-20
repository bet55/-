

export const fetchMovies = async () => {
    const url = document.baseURI.split('/')[2];
    const getMoviesUrl = `http://${url}/movies?format=json`.replace('#', '');
    const response = await fetch(getMoviesUrl);

    if (!response.ok) {
        const message = `Movies request error: ${response.status}`;
        console.error(message);
    }
    return await response.json();
}

