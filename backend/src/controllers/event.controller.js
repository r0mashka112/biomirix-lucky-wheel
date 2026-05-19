import { EventService } from "../services/event.service.js";

export class EventController {
    static async currentEvent(req, res, next) {
        try {
            const result = await EventService.getCurrentEvent();

            return res.json({
                success: true,
                message:
                    'Event fetched successfully',
                data: result
            });
        } catch (error) {
            next(error);
        }
    }
}