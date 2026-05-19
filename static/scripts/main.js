import { Wheel } from "./Wheel.js";
import { openModal } from './Modal.js';

document.addEventListener('DOMContentLoaded', async () => {
    const webApp = window.Telegram?.WebApp;
    const wheel = new Wheel();

    if (webApp) {
        webApp.ready();
        webApp.expand();

        const spinBtn = document.querySelector('[data-js-spin-button]');

        spinBtn.addEventListener('click', async () => {
            if (webApp.initData) {
                spinBtn.disabled = true;

                await wheel.spin(webApp.initData);

                spinBtn.disabled = false;
            } else {
                openModal('Работает только в Telegram')
            }
        });
    } else {
        openModal('Скрипт Telegram SDK не загрузился')
    }
});