'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {
    await queryInterface.createTable('users', {
      id: {
        type: Sequelize.BIGINT,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false
      },

      telegramId: {
        type: Sequelize.BIGINT,
        allowNull: false,
        unique: true
      },

      username: {
        type: Sequelize.STRING(64),
        allowNull: true
      },

      firstName: {
        type: Sequelize.STRING(128),
        allowNull: true
      },

      lastName: {
        type: Sequelize.STRING(128),
        allowNull: true
      },

      createdAt: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.fn('NOW')
      },

      updatedAt: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.fn('NOW')
      }
    });
  },

  async down (queryInterface, Sequelize) {
    await queryInterface.dropTable('users');
  }
};
