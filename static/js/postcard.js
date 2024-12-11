import {cartHandler} from "./postcard/movies_cart.js";


const savePostcard = () => {
    const saveButton = document.querySelector('#postcard-save-button');
    const posters = document.querySelectorAll('.poster');
    const title = document.querySelector('#invitation-title');

    saveButton.addEventListener('click', e => {
        title.contentEditable = false;

        const printCSS = '<link href="/static/css/postcard.css" rel="stylesheet" type="text/css">';
        window.frames["print_frame"].document.body.innerHTML = printCSS + document.querySelector('.postcard-container').innerHTML;
        window.frames["print_frame"].window.focus();
        window.frames["print_frame"].window.print();
    })


}

savePostcard();
cartHandler();