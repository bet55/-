const btnUp = {
    el: document.querySelector('.btn-up'),
    scrolling: false,
    show() {
        if (this.el.classList.contains('btn-hide') && !this.el.classList.contains('btn-hiding')) {
            this.el.classList.remove('btn-hide');
            this.el.classList.add('btn-hiding');
            window.setTimeout(() => {
                this.el.classList.remove('btn-hiding');
            }, 300);
        }
    },
    hide() {
        if (!this.el.classList.contains('btn-hide') && !this.el.classList.contains('btn-hiding')) {
            this.el.classList.add('btn-hiding');
            window.setTimeout(() => {
                this.el.classList.add('btn-hide');
                this.el.classList.remove('btn-hiding');
            }, 300);
        }
    },
    addEventListener() {
        // при прокрутке окна (window)
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY || document.documentElement.scrollTop;
            if (this.scrolling && scrollY > 0) {
                return;
            }
            this.scrolling = false;
            // если пользователь прокрутил страницу более чем на 200px
            if (scrollY > 400) {
                // сделаем кнопку .btn-up видимой
                this.show();
            } else {
                // иначе скроем кнопку .btn-up
                this.hide();
            }
        });
        // при нажатии на кнопку .btn-up
        document.querySelector('.btn-up').onclick = () => {
            this.scrolling = true;
            this.hide();
            // переместиться в верхнюю часть страницы
            window.scrollTo({
                top: 0,
                left: 0,
                behavior: 'smooth'
            });
        }
    }
}

export function showScrollButtonHandler() {
    btnUp.addEventListener();

}
