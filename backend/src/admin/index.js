import AdminJSExpress from '@adminjs/express'
import AdminJS, { ValidationError } from 'adminjs'
import * as AdminJSSequelize from '@adminjs/sequelize'

import { User, Event, Prize, Spin } from "../database/models/index.js";

AdminJS.registerAdapter({
    Resource: AdminJSSequelize.Resource,
    Database: AdminJSSequelize.Database
});

const adminOptions = {
    resources: [
        {
            resource: User,
            options: {
                id: 'users',
                listProperties: ['id', 'telegramId', 'username', 'firstName', 'lastName'],
                showProperties: ['id', 'telegramId', 'username', 'firstName', 'lastName', 'createdAt', 'updatedAt'],
                editProperties: ['telegramId', 'username', 'firstName', 'lastName'],
                sort: {
                    direction: 'desc',
                    sortBy: 'id'
                }
            }
        },
        {
            resource: Event,
            options: {
                id: 'events',
                listProperties: ['id', 'title', 'welcomeText', 'afterSpinText'],
                showProperties: ['id', 'title', 'welcomeText', 'afterSpinText', 'createdAt', 'updatedAt'],
                editProperties: ['title', 'welcomeText', 'afterSpinText']
            }
        },
        {
            resource: Prize,
            options: {
                id: 'prizes',
                listProperties: ['id', 'title', 'quantity', 'eventId'],
                showProperties: ['id', 'title', 'quantity', 'eventId', 'createdAt', 'updatedAt'],
                editProperties: ['title', 'quantity', 'eventId'],
                properties: {
                    id: {
                        isTitle: true
                    },
                    eventId: {
                        reference: 'events'
                    }
                }
            }
        },
        {
            resource: Spin,
            options: {
                id: 'spins',
                listProperties: ['id', 'userId', 'eventId', 'prizeId', 'createdAt'],
                showProperties: ['id', 'userId', 'eventId', 'prizeId', 'createdAt', 'updatedAt'],
                editProperties: ['userId', 'eventId', 'prizeId'],
                properties: {
                    id: {
                        isTitle: true
                    },
                    userId: {
                        reference: 'users'
                    },
                    eventId: {
                        reference: 'events'
                    },
                    prizeId: {
                        reference: 'prizes'
                    }
                }
            }
        }
    ],
    rootPath: '/admin',
    branding: {
        companyName: 'Biomirix Admin'
    }
}

export const adminJS = new AdminJS(adminOptions);

export const adminJSRouter = AdminJSExpress.buildRouter(adminJS);