import { Router } from "express";
import { EventController } from "../controllers/event.controller.js";

export const router = Router();

router.get(
    '/',
    EventController.currentEvent
);