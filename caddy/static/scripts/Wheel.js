import { openModal } from "./Modal.js";
import { WheelCanvas } from "./WheelCanvas.js";

const API_BASE_URL = "/api/v1";

async function requestApi(path, initData, options = {}) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        ...options,
        headers: {
            "X-Telegram-Init-Data": initData,
            ...(options.headers || {}),
        },
    });

    let data = null;
    try {
        data = await response.json();
    } catch (error) {
        data = null;
    }

    if (!response.ok) {
        const reason = data?.reason || "server_error";
        const apiError = new Error(reason);
        apiError.status = response.status;
        apiError.reason = reason;
        throw apiError;
    }

    return data;
}

export class Wheel {
    selectors = {
        wheel: "#wheel",
    };

    BASE_COLORS = [
        "#00446f",
        "#ed7102",
        "#ffffff",
    ];

    SECTORS_COUNT = 9;

    constructor() {
        this.wheelElement = document.querySelector(this.selectors.wheel);
        this.sectorColors = Array.from({ length: this.SECTORS_COUNT }, (_, i) =>
            this.BASE_COLORS[i % this.BASE_COLORS.length]
        );
        this.#init();
    }

    #init() {
        this.wheel = new WheelCanvas(this.wheelElement, this.sectorColors);
        return this.wheel;
    }

    async loadStatus(initData) {
        const webApp = window.Telegram?.WebApp;

        try {
            await requestApi("/me", initData);
            const status = await requestApi("/me/spin-status", initData);

            if (status.can_spin) {
                return {
                    canSpin: true,
                    reason: null,
                };
            }

            if (status.reason === "already_spun") {
                openModal(
                    `Вы уже участвовали. Ваш приз: ${status.spin.prize.name}`,
                    () => webApp?.close(),
                );
            } else if (status.reason === "no_prizes_left") {
                openModal("Призы закончились", () => webApp?.close());
            } else {
                openModal("Розыгрыш сейчас недоступен", () => webApp?.close());
            }

            return {
                canSpin: false,
                reason: status.reason,
            };
        } catch (error) {
            this.#handleError(error, webApp);
            return {
                canSpin: false,
                reason: error.reason || "server_error",
            };
        }
    }

    async spin(initData) {
        const webApp = window.Telegram?.WebApp;

        try {
            const spinData = await requestApi("/spins", initData, {
                method: "POST",
            });

            return new Promise(resolve => {
                const degrees = Math.ceil(Math.random() * 7200);
                this.wheel.spin(degrees, async () => {
                    openModal(`Вы выиграли приз: ${spinData.prize.name}`, () => {
                        webApp?.close();
                        resolve(true);
                    });
                });
            });
        } catch (error) {
            this.#handleError(error, webApp);
            return false;
        }
    }

    #handleError(error, webApp) {
        if (error.reason === "expired_init_data") {
            openModal("Сессия устарела, откройте приложение заново", () => webApp?.close());
        } else if (error.reason === "invalid_init_data") {
            openModal("Не удалось проверить Telegram-сессию", () => webApp?.close());
        } else if (error.status === 401) {
            openModal("Сессия Telegram недействительна", () => webApp?.close());
        } else if (error.reason === "already_spun") {
            openModal("Вы уже участвовали", () => webApp?.close());
        } else if (error.reason === "no_prizes_left") {
            openModal("Призы закончились", () => webApp?.close());
        } else {
            openModal("Сервис временно недоступен", () => webApp?.close());
        }
    }
}
