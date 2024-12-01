export const changeMovieArchiveStatus = (allMovies, movieId, target, posterContainer) => {
    const isArchive = document.URL.includes('archive');

    const removeUrl = '/movies/change_archive';
    const sendData = {kp_id: movieId, is_archive: !isArchive};

    fetch(removeUrl, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sendData)
    }).then(rs => rs.json()).then((data) => {
        console.log(data)
    }).catch(rs => {
        console.error(rs)
    });

    posterContainer.remove();
}
