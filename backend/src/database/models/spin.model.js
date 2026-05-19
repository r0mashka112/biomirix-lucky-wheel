import { DataTypes } from 'sequelize';
import { sequelize } from '../connection.js';

export const Spin = sequelize.define('Spin', {
    id: {
        type: DataTypes.BIGINT,
        primaryKey: true,
        autoIncrement: true
    },

    userId: {
        type: DataTypes.BIGINT,
        allowNull: false
    },

    eventId: {
        type: DataTypes.BIGINT,
        allowNull: false
    },

    prizeId: {
        type: DataTypes.BIGINT,
        allowNull: false
    }
}, {
    tableName: 'spins',

    indexes: [
        {
            unique: true,
            fields: ['userId', 'eventId']
        }
    ]
});