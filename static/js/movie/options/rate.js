import {getCookie} from "../../utils/cookie.js";
import {openModal} from "../rating_modal.js";

export const rateMovie = (allMovies, movieId, target, posterContainer) => {

    const user = getCookie('user')

    if (!user) {
        alert('Выберите пользователя')
    } else {
        openModal(movieId);
    }

}