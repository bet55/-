const createNoteElement = (movieId, userId, rating, comment) => {
    const userNote = document.querySelector(`.note-container[data-kp-id="${movieId}"] .note[data-user-id="${userId}"]`)
    console.log(userId, movieId);
    console.log(userNote);
    if (userNote) {
        console.log('exist')
        const noteH2 = userNote.querySelector('h2');
        // const noteP = userNote.querySelector('p');
        // noteP.textContent = comment;
        noteH2.textContent = rating;
        return false
    }
        console.log('not exist')
    const noteContainer = document.querySelector(`.note-container[data-kp-id="${movieId}"] `);
    const noteDiv = document.createElement('div');
    const noteH2 = document.createElement('h2');
    const noteP = document.createElement('p');


    noteP.textContent = comment;
    noteH2.textContent = rating;
    noteDiv.append(noteH2);
    noteDiv.classList.add('note');
    noteDiv.dataset.userId = userId

    noteContainer.append(noteDiv);
    return true;
}


const rateRequest = async (movieId, userId, rating, comment) => {
    const rateUrl = 'http://localhost:8000/movies/rate';
    const sendData = {
        user: userId,
        film: movieId,
        rating: rating,
    }

    if (comment) {
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
        console.error(sendData);
        console.error(e);
    }
}

export {createNoteElement, rateRequest}