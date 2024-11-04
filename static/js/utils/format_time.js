export const formatTime = (mins) => {
    let hours = Math.trunc(mins / 60);
    let minutes = mins % 60;
    return `${hours} часа ${minutes} минуты`;
}