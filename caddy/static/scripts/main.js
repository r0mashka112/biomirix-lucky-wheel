import { Wheel } from "./Wheel.js";
import { openModal } from "./Modal.js";

document.addEventListener("DOMContentLoaded", async () => {
    const webApp = window.Telegram?.WebApp;
    const spinBtn = document.querySelector("[data-js-spin-button]");
    const wheel = new Wheel();

    if (!spinBtn) {
        return;
    }

    const setButtonState = (text, disabled = false) => {
        spinBtn.textContent = text;
        spinBtn.disabled = disabled;
    };

    if (!webApp) {
        setButtonState("Недоступно", true);
        openModal("Скрипт Telegram SDK не загрузился");
        return;
    }

    webApp.ready();
    webApp.expand();

    if (!webApp.initData) {
        setButtonState("Недоступно", true);
        openModal("Откройте приложение через Telegram");
        return;
    }

    setButtonState("Загрузка...", true);

    const status = await wheel.loadStatus(webApp.initData);

    if (status?.canSpin) {
        setButtonState("Крутить", false);
    } else if (status?.reason === "already_spun") {
        setButtonState("Вы уже участвовали", true);
    } else {
        setButtonState("Недоступно", true);
    }

    spinBtn.addEventListener("click", async () => {
        setButtonState("Крутим...", true);

        const spinWasCompleted = await wheel.spin(webApp.initData);

        if (spinWasCompleted) {
            setButtonState("Вы уже участвовали", true);
            return;
        }

        setButtonState("Крутить", false);
    });
});
