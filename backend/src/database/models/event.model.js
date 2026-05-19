import { DataTypes } from 'sequelize';
import { sequelize } from '../connection.js';

export const Event = sequelize.define('Event', {
    id: {
        type: DataTypes.BIGINT,
        primaryKey: true,
        autoIncrement: true
    },

    title: {
        type: DataTypes.STRING(255),
        allowNull: false
    },

    welcomeText: {
        type: DataTypes.TEXT,
        allowNull: true
    },

    afterSpinText: {
        type: DataTypes.TEXT,
        allowNull: true
    }
}, {
    tableName: 'events'
});