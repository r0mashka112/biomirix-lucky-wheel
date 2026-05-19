import { env } from './env.config.js';

export const serverConfig = {
    host: env.SERVER_HOST || '0.0.0.0',
    port: parseInt(env.SERVER_PORT) || 3000
}