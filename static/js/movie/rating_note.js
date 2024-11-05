const createNoteElement = (movieId, rating, comment) => {

    const noteContainer = document.querySelector(`.note-container[data-kp-id="${movieId}"] `);
    const noteDiv = document.createElement('div');
    const noteH2 = document.createElement('h2');
    const noteP = document.createElement('p');


    noteP.textContent = comment;
    noteH2.textContent = rating;
    noteDiv.append(noteH2);
    noteDiv.classList.add('note');

    noteContainer.append(noteDiv);
}


const rateRequest = async (movieId, userId, rating, comment) => {
    const rateUrl = 'http://localhost:8000/movies/rate';
    const sendData = {
        user: userId,
        film: movieId,
        rating: rating,
    }

    if(comment) {
        sendData['text'] = comment;
    }


    try {
        const response = await fetch(rateUrl, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sendData),
        });
        console.log(await response.json());
    } catch (e) {
        console.error(e);
    }
}

export {createNoteElement, rateRequest}