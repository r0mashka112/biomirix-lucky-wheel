import { Event } from '../database/models/index.js';

export class EventService {
    static async getCurrentEvent() {
        const event = await Event.findOne();

        if (!event) {
            const error = new Error('Event not found');

            error.status = 404;
            error.code = 'EVENT_NOT_FOUND';

            throw error;
        }

        return {
            id: event.id,
            title: event.title,
            welcomeText: event.welcomeText,
            afterSpinText: event.afterSpinText
        };
    }
}