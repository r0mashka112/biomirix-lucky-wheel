import { SpinService } from "../services/spin.service.js";

export class SpinController {
    static async spin(req, res, next) {
        try {
            const result = await SpinService.spin({
                telegramUser: req.telegramUser
            });

            return res.json({
                success: true,
                message:
                    'Spin completed successfully',
                data: result
            });
        } catch (error) {
            next(error);
        }
    }
}