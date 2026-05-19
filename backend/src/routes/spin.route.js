import { Router } from "express";
import { SpinController } from "../controllers/spin.controller.js";
import { telegramAuthMiddleware } from "../middlewares/telegramAuth.middleware.js";

export const router = Router();

router.post(
    '/',
    telegramAuthMiddleware,
    SpinController.spin
);