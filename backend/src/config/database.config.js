import { env } from './env.config.js';

export const databaseConfig = {
    username: env.DATABASE_USERNAME || "postgres",
    password: env.DATABASE_PASSWORD || "",
    database: env.DATABASE_NAME || "biomirix",
    host: env.DATABASE_HOST || "db",
    port: parseInt(env.DATABASE_PORT) || 5432,
    dialect: 'postgres',
    logging: false,
    benchmark: false,
    logQueryParameters: false,
    pool: {
        max: 15,
        min: 2,
        acquire: 30000,
        idle: 10000,
        evict: 5000
    },
    retry: {
        max: 3,
        match: [
            /SequelizeConnectionError/,
            /SequelizeConnectionAcquireTimeoutError/,
            /SequelizeConnectionRefusedError/,
            /Connection terminated unexpectedly/
        ]
    },
    dialectOptions: {
        statement_timeout: 5000,
        idle_in_transaction_session_timeout: 10000,

        keepAlive: true,
        keepAliveInitialDelayMillis: 10000
    }
}