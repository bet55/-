const form = document.querySelector("#movie-saver");

async function sendData() {
    // Associate the FormData object with the form element
    const formData = new FormData(form);
    const addUrl = 'http://localhost:8000/movies/add';

    try {
        const response = await fetch(addUrl, {
            method: "POST",
            // Set the FormData instance as the request body
            body: formData,
        });
        console.log(await response.json());
    } catch (e) {
        console.error(e);
    }
}

// Take over form submission
form.addEventListener("submit", (event) => {
    event.preventDefault();
    sendData();
});
