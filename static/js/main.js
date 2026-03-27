document.addEventListener('DOMContentLoaded', () => {
    initHamburger();
    initSmoothScroll();
    initScrollTopBtn();
    initStickyNav();
});

function initHamburger() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeBtn = document.getElementById('mobileMenuClose');
    if (!hamburger || !mobileMenu) return;

    const toggle = (open) => {
        mobileMenu.classList.toggle('is-open', open);
        hamburger.classList.toggle('is-active', open);
        document.body.style.overflow = open ? 'hidden' : '';
    };

    hamburger.addEventListener('click', () => toggle(true));
    if (closeBtn) closeBtn.addEventListener('click', () => toggle(false));

    mobileMenu.querySelectorAll('.mobile-menu__link').forEach(link => {
        link.addEventListener('click', () => toggle(false));
    });

    mobileMenu.addEventListener('click', (e) => {
        if (e.target === mobileMenu) toggle(false);
    });
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const targetId = anchor.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (!target) return;

            e.preventDefault();
            const headerOffset = parseInt(
                getComputedStyle(document.documentElement)
                    .getPropertyValue('--header-height'), 10
            ) || 70;

            const top = target.getBoundingClientRect().top + window.scrollY - headerOffset;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });
}

function initScrollTopBtn() {
    const btn = document.getElementById('scrollTopBtn');
    if (!btn) return;

    const checkScroll = () => {
        btn.classList.toggle('is-visible', window.scrollY > 400);
    };

    window.addEventListener('scroll', checkScroll, { passive: true });
    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

function initStickyNav() {
    const nav = document.querySelector('.nav');
    if (!nav) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const current = window.scrollY;
        if (current > 100) {
            nav.style.backgroundColor = 'rgba(15, 18, 16, 0.98)';
        } else {
            nav.style.backgroundColor = 'rgba(15, 18, 16, 0.95)';
        }
        lastScroll = current;
    }, { passive: true });
}
