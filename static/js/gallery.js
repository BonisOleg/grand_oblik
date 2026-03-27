document.addEventListener('DOMContentLoaded', () => {
    initGalleryFilters();
    initLightbox();
});

function initGalleryFilters() {
    const filters = document.querySelectorAll('.gallery-filter');
    const items = document.querySelectorAll('.gallery-item');

    filters.forEach(btn => {
        btn.addEventListener('click', () => {
            const cat = btn.dataset.category;

            filters.forEach(f => f.classList.remove('is-active'));
            btn.classList.add('is-active');

            items.forEach(item => {
                if (cat === 'all' || item.dataset.category === cat) {
                    item.dataset.hidden = 'false';
                    item.style.display = '';
                } else {
                    item.dataset.hidden = 'true';
                    item.style.display = 'none';
                }
            });
        });
    });
}

function initLightbox() {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;

    const img = lightbox.querySelector('.lightbox__img');
    const caption = lightbox.querySelector('.lightbox__caption');
    const counter = lightbox.querySelector('.lightbox__counter');
    const closeBtn = lightbox.querySelector('.lightbox__close');
    const prevBtn = lightbox.querySelector('.lightbox__arrow--prev');
    const nextBtn = lightbox.querySelector('.lightbox__arrow--next');

    let images = [];
    let currentIdx = 0;

    function getVisibleItems() {
        return [...document.querySelectorAll('.gallery-item:not([data-hidden="true"]), .perspective-mini-gallery__item')];
    }

    function open(idx) {
        images = getVisibleItems().map(item => ({
            src: item.querySelector('img').src,
            alt: item.querySelector('img').alt || '',
        }));
        currentIdx = idx;
        show();
        lightbox.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }

    function close() {
        lightbox.classList.remove('is-open');
        document.body.style.overflow = '';
    }

    function show() {
        if (!images[currentIdx]) return;
        img.src = images[currentIdx].src;
        img.alt = images[currentIdx].alt;
        if (caption) caption.textContent = images[currentIdx].alt;
        if (counter) counter.textContent = `${currentIdx + 1} / ${images.length}`;
    }

    function next() {
        currentIdx = (currentIdx + 1) % images.length;
        show();
    }

    function prev() {
        currentIdx = (currentIdx - 1 + images.length) % images.length;
        show();
    }

    document.addEventListener('click', (e) => {
        const item = e.target.closest('.gallery-item, .perspective-mini-gallery__item');
        if (!item) return;
        const allVisible = getVisibleItems();
        const idx = allVisible.indexOf(item);
        if (idx !== -1) open(idx);
    });

    if (closeBtn) closeBtn.addEventListener('click', close);
    if (prevBtn) prevBtn.addEventListener('click', prev);
    if (nextBtn) nextBtn.addEventListener('click', next);

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) close();
    });

    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('is-open')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowRight') next();
        if (e.key === 'ArrowLeft') prev();
    });

    let touchStartX = 0;
    lightbox.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
    }, { passive: true });

    lightbox.addEventListener('touchend', (e) => {
        const diff = touchStartX - e.changedTouches[0].clientX;
        if (Math.abs(diff) > 50) {
            diff > 0 ? next() : prev();
        }
    });
}
