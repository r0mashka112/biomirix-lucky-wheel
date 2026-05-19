import { User } from './user.model.js';
import { Spin } from './spin.model.js';
import { Event } from './event.model.js';
import { Prize } from './prize.model.js';

User.hasMany(Spin, {
    foreignKey: 'userId'
});

Spin.belongsTo(User, {
    foreignKey: 'userId'
});

Event.hasMany(Prize, {
    foreignKey: 'eventId'
});

Prize.belongsTo(Event, {
    foreignKey: 'eventId'
});

Event.hasMany(Spin, {
    foreignKey: 'eventId'
});

Spin.belongsTo(Event, {
    foreignKey: 'eventId'
});

Prize.hasMany(Spin, {
    foreignKey: 'prizeId'
});

Spin.belongsTo(Prize, {
    foreignKey: 'prizeId'
});

export {
    User,
    Event,
    Prize,
    Spin
};