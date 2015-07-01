"""link all tables to user

Revision ID: 22408821e8b2
Revises: 19602cc4f40
Create Date: 2015-06-28 08:24:21.866459

"""

# revision identifiers, used by Alembic.
revision = '22408821e8b2'
down_revision = '19602cc4f40'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, ForeignKey, Boolean


def upgrade():
    op.add_column('brand', Column('user_id', Integer, ForeignKey('user.id')))
    op.add_column('commodity_meta', Column('user_id', Integer, ForeignKey('user.id')))
    op.add_column('discount', Column('user_id', Integer, ForeignKey('user.id')))
    op.add_column('upload_file', Column('user_id', Integer, ForeignKey('user.id')))
    pass


def downgrade():
    op.drop_constraint('brand_ibfk_1', 'brand', 'foreignkey')
    op.drop_column('brand', 'user_id')
    op.drop_constraint('commodity_meta_ibfk_1', 'commodity_meta', 'foreignkey')
    op.drop_column('commodity_meta', 'user_id')
    op.drop_constraint('discount_ibfk_1', 'discount', 'foreignkey')
    op.drop_column('discount', 'user_id')
    op.drop_constraint('upload_file_ibfk_1', 'upload_file', 'foreignkey')
    op.drop_column('upload_file', 'user_id')
    pass
