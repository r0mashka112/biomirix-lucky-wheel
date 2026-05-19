import { Op } from "sequelize";
import { botConfig } from "../config/bot.config.js";
import { sequelize } from '../database/connection.js';
import {
    User,
    Event,
    Prize,
    Spin
} from '../database/models/index.js';

export class SpinService {
    static async spin({ telegramUser }) {
        const event = await Event.findOne();

        if (!event) {
            const error = new Error(
                'Event not found'
            );

            error.status = 404;
            error.code = 'EVENT_NOT_FOUND';

            throw error;
        }

        const [user] = await User.findOrCreate({
            where: {
                telegramId: telegramUser.telegramId
            },

            defaults: {
                username: telegramUser.username,
                firstName: telegramUser.firstName,
                lastName: telegramUser.lastName
            }
        });

        const transaction = await sequelize.transaction();

        try {
            const existingSpin = await Spin.findOne({
                where: {
                    userId: user.id,
                    eventId: event.id
                },

                transaction,

                lock: transaction.LOCK.UPDATE
            });

            if (existingSpin) {
                const error = new Error(
                    'User already spun'
                );

                error.status = 400;
                error.code = 'USER_ALREADY_SPUN';

                throw error;
            }

            const prizes = await Prize.findAll({
                where: {
                    eventId: event.id,
                    quantity: {
                        [Op.gt]: 0
                    }
                },

                transaction,

                lock: transaction.LOCK.UPDATE
            });

            if (!prizes.length) {
                const error = new Error(
                    'No prizes left'
                );

                error.status = 400;
                error.code = 'NO_PRIZES_LEFT';

                throw error;
            }

            const randomPrize = prizes[
                Math.floor(Math.random() * prizes.length)
            ];

            await randomPrize.decrement(
                'quantity',
                {
                    by: 1,
                    transaction
                }
            );

            const spin = await Spin.create({
                userId: user.id,
                eventId: event.id,
                prizeId: randomPrize.id
            }, {
                transaction
            });

            await transaction.commit();

            const result = {
                spinId: spin.id,
                prize: {
                    id: randomPrize.id,
                    title: randomPrize.title
                }
            };

            this.#sendNotificationToBot(user.telegramId, result.prize.title, event.afterSpinText).catch(error => {
                console.error('Failed to send bot notification:', error);
            });

            return result;
        } catch (error) {
            await transaction.rollback();
            throw error;
        }
    }

    static async #sendNotificationToBot(telegramId, prize, afterSpinText) {
        try {
            const baseMessage = `🎉 <b>Поздравляем с выигрышем!</b> 🎉
✨ Вы выиграли: <b>${prize}</b> ✨

Спасибо, что приняли участие в розыгрыше призов от Biomirix! 🎡`;

            const sendNotification = async (message) => {
                await fetch(`https://api.telegram.org/bot${botConfig.token}/sendMessage`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        chat_id: telegramId,
                        text: message,
                        parse_mode: 'HTML'
                    })
                });
            }
            
            await sendNotification(baseMessage);

            if (afterSpinText) {
                await sendNotification(afterSpinText);
            }

        } catch (error) {
            console.error('Error sending bot notification:', error);
        }
    }
}