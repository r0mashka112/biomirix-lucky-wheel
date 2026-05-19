import { DataTypes } from 'sequelize';
import { sequelize } from '../connection.js';

export const Prize = sequelize.define('Prize', {
    id: {
        type: DataTypes.BIGINT,
        primaryKey: true,
        autoIncrement: true
    },

    eventId: {
        type: DataTypes.BIGINT,
        allowNull: false
    },

    title: {
        type: DataTypes.STRING(255),
        allowNull: false,
        validate: {
            notEmpty: {
                msg: 'The name of the prize is required'
            },
            len: {
                args: [1, 255],
                msg: 'The name must be between 1 and 255 characters'
            }
        }
    },

    quantity: {
        type: DataTypes.INTEGER,
        allowNull: false,
        defaultValue: 0,
        validate: {
            min: {
                args: [0],
                msg: 'The quantity cannot be negative'
            },
            isInt: {
                msg: 'Quantity must be a number'
            }
        }
    }
}, {
    tableName: 'prizes'
});