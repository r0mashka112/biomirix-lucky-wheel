import express from 'express';

import {
    sequelize
} from "./database/connection.js";

import {
    serverConfig
} from "./config/server.config.js";

import {
    adminJS,
    adminJSRouter
} from "./admin/index.js";

import {
    router as spinRouter
} from "./routes/spin.route.js";

import {
    router as eventRouter
} from "./routes/event.route.js";

import {
    errorMiddleware
} from "./middlewares/error.middleware.js";

const startServer = async () => {
    try {
        const app = express();
        app.use(express.json());
        app.use(express.urlencoded({
            extended: true
        }));

        app.use('/api/spin', spinRouter);
        app.use('/api/event', eventRouter);

        app.use(
            adminJS.options.rootPath,
            adminJSRouter
        );

        app.use(errorMiddleware);

        await sequelize.authenticate();

        app.listen(serverConfig.port, serverConfig.host, () => {
            console.log(`Server running...`);
        });
    } catch (error) {
        console.error('Failed to start server:', error);
        process.exit(1);
    }
};

const stopServer = async () => {
    console.log('\nShutting down gracefully...');

    try {
        await sequelize.close();
        console.log('Database connection closed');
        process.exit(0);
    } catch (error) {
        console.error('Error during shutdown:', error);
        process.exit(1);
    }
};

process.on('SIGTERM', stopServer);
process.on('SIGINT', stopServer);

await startServer();