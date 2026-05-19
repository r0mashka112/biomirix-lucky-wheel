'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('prizes', {
      id: {
        type: Sequelize.BIGINT,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false
      },

      eventId: {
        type: Sequelize.BIGINT,
        allowNull: false,

        references: {
          model: 'events',
          key: 'id'
        },

        onDelete: 'CASCADE',
        onUpdate: 'CASCADE'
      },

      title: {
        type: Sequelize.STRING(255),
        allowNull: false
      },

      quantity: {
        type: Sequelize.INTEGER,
        allowNull: false,
        defaultValue: 0
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

    await queryInterface.addIndex(
        'prizes',
        ['eventId'],
        {
          name: 'prizes_event_id_index'
        }
    );
  },

  async down(queryInterface) {
    await queryInterface.dropTable('prizes');
  }
};