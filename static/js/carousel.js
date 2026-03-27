document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.carousel').forEach(el => new Carousel(el));
});

class Carousel {
    constructor(el) {
        this.el = el;
        this.track = el.querySelector('.carousel__track');
        this.slides = [...el.querySelectorAll('.carousel__slide')];
        this.currentIndex = 0;
        this.startX = 0;
        this.currentX = 0;
        this.isDragging = false;

        if (this.slides.length < 2) return;

        this.calcSlidesPerView();
        this.createNav();
        this.bindTouch();
        this.bindResize();
        this.goTo(0);
    }

    calcSlidesPerView() {
        const w = window.innerWidth;
        if (w >= 1024) this.perView = 3;
        else if (w >= 768) this.perView = 2;
        else this.perView = 1;
        this.maxIndex = Math.max(0, this.slides.length - this.perView);
    }

    createNav() {
        const existing = this.el.querySelector('.carousel__nav');
        if (existing) existing.remove();

        const nav = document.createElement('div');
        nav.className = 'carousel__nav';

        const prevBtn = document.createElement('button');
        prevBtn.className = 'carousel__arrow';
        prevBtn.setAttribute('aria-label', 'Попередній');
        prevBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>';
        prevBtn.addEventListener('click', () => this.prev());

        const nextBtn = document.createElement('button');
        nextBtn.className = 'carousel__arrow';
        nextBtn.setAttribute('aria-label', 'Наступний');
        nextBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>';
        nextBtn.addEventListener('click', () => this.next());

        const dots = document.createElement('div');
        dots.className = 'carousel__dots';

        for (let i = 0; i <= this.maxIndex; i++) {
            const dot = document.createElement('button');
            dot.className = 'carousel__dot';
            dot.setAttribute('aria-label', `Слайд ${i + 1}`);
            dot.addEventListener('click', () => this.goTo(i));
            dots.appendChild(dot);
        }

        nav.appendChild(prevBtn);
        nav.appendChild(dots);
        nav.appendChild(nextBtn);
        this.el.appendChild(nav);

        this.dots = [...dots.querySelectorAll('.carousel__dot')];
        this.updateDots();
    }

    bindTouch() {
        this.track.addEventListener('touchstart', (e) => {
            this.isDragging = true;
            this.startX = e.touches[0].clientX;
            this.track.classList.add('is-dragging');
        }, { passive: true });

        this.track.addEventListener('touchmove', (e) => {
            if (!this.isDragging) return;
            this.currentX = e.touches[0].clientX;
        }, { passive: true });

        this.track.addEventListener('touchend', () => {
            if (!this.isDragging) return;
            this.isDragging = false;
            this.track.classList.remove('is-dragging');
            const diff = this.startX - this.currentX;
            if (Math.abs(diff) > 50) {
                diff > 0 ? this.next() : this.prev();
            }
        });

        this.track.addEventListener('mousedown', (e) => {
            this.isDragging = true;
            this.startX = e.clientX;
            this.track.classList.add('is-dragging');
        });

        document.addEventListener('mousemove', (e) => {
            if (!this.isDragging) return;
            this.currentX = e.clientX;
        });

        document.addEventListener('mouseup', () => {
            if (!this.isDragging) return;
            this.isDragging = false;
            this.track.classList.remove('is-dragging');
            const diff = this.startX - this.currentX;
            if (Math.abs(diff) > 50) {
                diff > 0 ? this.next() : this.prev();
            }
        });
    }

    bindResize() {
        let timeout;
        window.addEventListener('resize', () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                this.calcSlidesPerView();
                this.createNav();
                this.goTo(Math.min(this.currentIndex, this.maxIndex));
            }, 200);
        });
    }

    goTo(index) {
        this.currentIndex = Math.max(0, Math.min(index, this.maxIndex));
        const pct = -(this.currentIndex * (100 / this.perView));
        this.track.style.transform = `translateX(${pct}%)`;
        this.updateDots();
    }

    next() {
        this.goTo(this.currentIndex + 1);
    }

    prev() {
        this.goTo(this.currentIndex - 1);
    }

    updateDots() {
        if (!this.dots) return;
        this.dots.forEach((d, i) => {
            d.classList.toggle('is-active', i === this.currentIndex);
        });
    }
}
