export const removeMovie = (allMovies, movieId, target, posterContainer) => {

    const removeUrl = '/movies/remove';
    const sendData = {kp_id: movieId};

    fetch(removeUrl, {
        method: 'DELETE',
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