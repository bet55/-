import {setCookie} from "../utils/cookie.js";

const usersSelector = document.querySelector('#users-select');

export function settingUserHandler() {
    usersSelector.addEventListener('change', (event) => {
        const user = usersSelector.value;
        setCookie('user', user)

    })

}