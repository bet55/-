const addButton = document.querySelector("#button");
const input = document.querySelector("#form");

async function sendData() {
    // Associate the FormData object with the form element
    const sendData = {
        kp_id: input.value
    };
    const addUrl = 'http://localhost:8000/movies/add';

    try {
        const response = await fetch(addUrl, {
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

    input.value = '';
}

// Take over form submission
addButton.addEventListener("click", (event) => {
    event.preventDefault();
    sendData();
});
