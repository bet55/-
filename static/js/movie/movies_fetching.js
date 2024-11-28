

export const fetchMovies = async () => {
    const getMoviesUrl = 'http://localhost:8000/movies?format=json'
    // const getMoviesUrl = document.URL + '?format=json'

    console.log(getMoviesUrl);
    const response = await fetch(getMoviesUrl);

    if (!response.ok) {
        const message = `Movies request error: ${response.status}`;
        console.error(message);
    }
    return await response.json();
}

