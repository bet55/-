import {cartMoviesHandler} from "./based_layout/movies_cart.js";
import {settingUserHandler} from "./based_layout/setup_user.js";

// Активируем подсказки элементов
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

settingUserHandler(); // выбор пользователя
cartMoviesHandler(); // корзина с выбранными фильмами
// showScrollButtonHandler() // кнопка скролла наверх

