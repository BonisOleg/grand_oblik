/**
 * HTMX 2 за замовчуванням не робить swap для 4xx — форма з помилками (422) не оновлювалась.
 * Дозволяємо swap лише для 422 (валідація форми).
 */
(function () {
    function patchResponseHandling() {
        if (!window.htmx || !htmx.config) return;
        htmx.config.responseHandling = [
            { code: '204', swap: false },
            { code: '[23]..', swap: true },
            { code: '422', swap: true },
            { code: '[45]..', swap: false, error: true },
        ];
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', patchResponseHandling);
    } else {
        patchResponseHandling();
    }
})();
