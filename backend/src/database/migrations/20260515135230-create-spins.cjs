'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('spins', {
      id: {
        type: Sequelize.BIGINT,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false
      },

      userId: {
        type: Sequelize.BIGINT,
        allowNull: false,

        references: {
          model: 'users',
          key: 'id'
        },

        onDelete: 'CASCADE',
        onUpdate: 'CASCADE'
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

      prizeId: {
        type: Sequelize.BIGINT,
        allowNull: false,

        references: {
          model: 'prizes',
          key: 'id'
        },

        onDelete: 'CASCADE',
        onUpdate: 'CASCADE'
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
        'spins',
        ['userId', 'eventId'],
        {
          unique: true,
          name: 'spins_user_event_unique'
        }
    );

    await queryInterface.addIndex(
        'spins',
        ['eventId'],
        {
          name: 'spins_event_id_index'
        }
    );

    await queryInterface.addIndex(
        'spins',
        ['prizeId'],
        {
          name: 'spins_prize_id_index'
        }
    );
  },

  async down(queryInterface) {
    await queryInterface.dropTable('spins');
  }
};