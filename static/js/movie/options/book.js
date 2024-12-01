import {bookedToggle} from "../booked_toggler.js";
import {addToCart, removeFromCart} from "../../based_layout/movies_cart.js";

export const addMovieToBookmark = (allMovies, movieId, target, posterContainer) => {
    if (target.classList.contains('booked')) {
        bookedToggle(movieId, true);
        removeFromCart(movieId);


    } else {
        bookedToggle(movieId);
        addToCart(movieId, allMovies[movieId]);
    }

}
