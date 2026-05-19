import { Sequelize } from 'sequelize';
import { databaseConfig } from '../config/database.config.js';

export const sequelize = new Sequelize(databaseConfig);
