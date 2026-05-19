import { openModal } from './Modal.js';
import { WheelCanvas } from "./WheelCanvas.js";

export class Wheel {
    selectors = {
        wheel: '#wheel'
    };

    BASE_COLORS = [
        '#00446f',
        '#ed7102',
        '#ffffff'
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

    async spin(initData) {
        const webApp = window.Telegram?.WebApp;

        try {
            const response = await fetch('/api/spin', {
                method: 'POST',
                headers: {
                    'X-Telegram-Init-Data': initData,
                }
            });

            const result = await response.json();

            if (!result.success) {
                if (result.code === 'EVENT_NOT_FOUND') {
                    openModal('Розыгрыш завершился', () => webApp.close());
                } else if (result.code === 'USER_ALREADY_SPUN') {
                    openModal('Вы уже вращали колесо', () => webApp.close());
                } else if (result.code === 'NO_PRIZES_LEFT') {
                    openModal('Призы закончились', () => webApp.close());
                } else if (result.code === 'INTERNAL_SERVER_ERROR') {
                    openModal('Непредвиденная ошибка от сервера', () => webApp.close());
                }

                return;
            }

            const spinData = result.data;

            return new Promise(resolve => {
                const degrees = Math.ceil(Math.random() * 7200);
                this.wheel.spin(degrees, async () => {
                    openModal(`Вы выиграли приз: ${spinData.prize.title}`, () => {
                        webApp.close();
                        resolve();
                    });
                });
            });
        } catch (error) {
            openModal('Произошла ошибка. Попробуйте позже.', () => webApp.close());
        }
    }
}
