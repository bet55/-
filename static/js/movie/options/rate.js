import {getCookie} from "../../utils/cookie.js";
import {showUserRequiredModal} from "../../utils/show_modal.js";
import {showRatingModal} from "../rating_modal.js";

export const rateMovie = (allMovies, movieId, target, posterContainer) => {

    const user = getCookie('user')

    if (!user) {
        showUserRequiredModal();
    } else {
        showRatingModal(movieId);
    }

}