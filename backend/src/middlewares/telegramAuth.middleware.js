import {
    validateAndParseInitData,
    getBotTokenSecretKey
} from '@gramio/init-data';
import { botConfig } from "../config/bot.config.js";

const secretKey = getBotTokenSecretKey(
    botConfig.token
);

export const telegramAuthMiddleware = (
    req,
    res,
    next
) => {
    try {
        const initData = req.headers['x-telegram-init-data'];

        if (!initData) {
            return res.status(400).json({
                success: false,
                message: 'Missing Telegram init data',
                code: 'MISSING_INIT_DATA'
            });
        }

        const result = validateAndParseInitData(
            initData,
            secretKey
        );

        if (!result || !result.user) {
            return res.status(401).json({
                success: false,
                message: 'Invalid Telegram init data',
                code: 'INVALID_INIT_DATA'
            });
        }

        const now = Math.floor(Date.now() / 1000);

        if (now - result.auth_date > 3600) {
            return res.status(401).json({
                success: false,
                message: 'Init data expired',
                code: 'INIT_DATA_EXPIRED'
            });
        }

        req.telegramUser = {
            telegramId: result.user.id,
            username: result.user.username,
            firstName: result.user.first_name,
            lastName: result.user.last_name
        };

        next();
    } catch (error) {
        return res.status(401).json({
            success: false,
            message: error.message || 'Authentication failed',
            code: 'AUTH_FAILED'
        });
    }
};