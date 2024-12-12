export const formatTime = (mins) => {
    let hours = Math.trunc(mins / 60);
    let minutes = mins % 60;

    if(!hours) {
        hours = '~';
        minutes = '~';
    }
    return `${hours} часа ${minutes} минуты`;
}