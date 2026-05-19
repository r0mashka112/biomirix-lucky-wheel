import { DataTypes } from 'sequelize';
import { sequelize } from "../connection.js";

export const User = sequelize.define('User', {
    id: {
        type: DataTypes.BIGINT,
        primaryKey: true,
        autoIncrement: true
    },

    telegramId: {
        type: DataTypes.BIGINT,
        allowNull: false,
        unique: true
    },

    username: {
        type: DataTypes.STRING(64),
        allowNull: true
    },

    firstName: {
        type: DataTypes.STRING(128),
        allowNull: true
    },

    lastName: {
        type: DataTypes.STRING(128),
        allowNull: true
    }
}, {
    tableName: 'users',
    indexes: [
        {
            unique: true,
            fields: ['telegramId']
        }
    ]
});