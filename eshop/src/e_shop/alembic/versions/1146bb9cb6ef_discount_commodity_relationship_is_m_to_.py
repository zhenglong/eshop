"""discount & commodity relationship is m-to-m

Revision ID: 1146bb9cb6ef
Revises: 1f5d61e83c65
Create Date: 2015-06-01 21:18:34.252536

"""

# revision identifiers, used by Alembic.
revision = '1146bb9cb6ef'
down_revision = '1f5d61e83c65'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, Integer, ForeignKey, Boolean

def upgrade():
    op.drop_constraint('discount_ibfk_1', 'discount', 'foreignkey')
    op.drop_column('discount', 'commodity_id')
    op.add_column('commodity', Column('is_off_shelve', Boolean, default=False))
    pass


def downgrade():
    op.add_column('discount', Column('commodity_id', Integer, ForeignKey('commodity.id')))
    op.drop_column('commodity', 'is_off_shelve')
    pass
