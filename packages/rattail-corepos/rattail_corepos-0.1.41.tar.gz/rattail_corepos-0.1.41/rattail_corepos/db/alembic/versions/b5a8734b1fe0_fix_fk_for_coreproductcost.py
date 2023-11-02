# -*- coding: utf-8; -*-
"""fix FK for CoreProductCost

Revision ID: b5a8734b1fe0
Revises: 15bf65f68c52
Create Date: 2023-10-20 11:20:09.231682

"""

# revision identifiers, used by Alembic.
revision = 'b5a8734b1fe0'
down_revision = '15bf65f68c52'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_product_cost
    op.alter_column('corepos_product_cost', 'corepos_id', existing_type=sa.INTEGER(), nullable=True)
    op.add_column('corepos_product_cost', sa.Column('corepos_vendor_id', sa.Integer(), nullable=False))
    op.add_column('corepos_product_cost', sa.Column('corepos_sku', sa.String(length=13), nullable=False))
    op.add_column('corepos_product_cost_version', sa.Column('corepos_vendor_id', sa.Integer(), autoincrement=False, nullable=True))
    op.add_column('corepos_product_cost_version', sa.Column('corepos_sku', sa.String(length=13), autoincrement=False, nullable=True))


def downgrade():

    # corepos_product_cost
    op.drop_column('corepos_product_cost_version', 'corepos_sku')
    op.drop_column('corepos_product_cost_version', 'corepos_vendor_id')
    op.drop_column('corepos_product_cost', 'corepos_sku')
    op.drop_column('corepos_product_cost', 'corepos_vendor_id')
    op.alter_column('corepos_product_cost', 'corepos_id', existing_type=sa.INTEGER(), nullable=False)
