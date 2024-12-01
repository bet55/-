import {setCookie} from "../utils/cookie.js";

const usersSelector = document.querySelector('#users-selector');

export function settingUserHandler() {
    const usersElements = usersSelector.querySelectorAll('.dropdown-item');

    usersElements.forEach(e => {
        e.addEventListener('click', e => {
            const user = e.target.dataset.userId;
            setCookie('user', user)
        })
    })


}