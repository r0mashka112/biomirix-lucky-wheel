'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('events', {
      id: {
        type: Sequelize.BIGINT,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false
      },

      title: {
        type: Sequelize.STRING(255),
        allowNull: false
      },

      welcomeText: {
        type: Sequelize.TEXT,
        allowNull: true
      },

      afterSpinText: {
        type: Sequelize.TEXT,
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

  async down(queryInterface) {
    await queryInterface.dropTable('events');
  }
};