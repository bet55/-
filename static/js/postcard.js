import {cartHandler} from "./postcard/movies_cart.js";
import {createToast} from "./utils/create_toast.js";

const screenShot = () => {
    let div = document.getElementById('postcard-container');
    html2canvas(div).then(
        function (canvas) {
            document
                .getElementById('output')
                .appendChild(canvas);
        })
}

const savePostcard = () => {
    const saveButton = document.querySelector('#postcard-save-button');
    const posters = document.querySelectorAll('.poster');
    const title = document.querySelector('#invitation-title');


    saveButton.addEventListener('click', e => {
        if (title.innerText.replace(/\D/g, '').length < 1) {
            createToast('Введите дату церемонии', 'error')
        } else {
            title.contentEditable = false;
        }
    })


}

savePostcard();
cartHandler();