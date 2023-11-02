# -*- coding: utf-8; -*-
"""add core_member.corepos_card_number

Revision ID: 15bf65f68c52
Revises: 673ff7088d35
Create Date: 2023-10-12 07:39:34.608105

"""

# revision identifiers, used by Alembic.
revision = '15bf65f68c52'
down_revision = '673ff7088d35'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_member
    op.alter_column('corepos_member', 'corepos_account_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('corepos_member', sa.Column('corepos_card_number', sa.Integer(), nullable=True))
    op.add_column('corepos_member_version', sa.Column('corepos_card_number', sa.Integer(), autoincrement=False, nullable=True))

def downgrade():

    # corepos_member
    op.drop_column('corepos_member_version', 'corepos_card_number')
    op.drop_column('corepos_member', 'corepos_card_number')
    op.alter_column('corepos_member', 'corepos_account_id',
               existing_type=sa.INTEGER(),
               nullable=False)
