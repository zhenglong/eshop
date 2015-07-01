"""add column auth_user_id to table user

Revision ID: 19602cc4f40
Revises: 1146bb9cb6ef
Create Date: 2015-06-28 01:15:16.507924

"""

# revision identifiers, used by Alembic.
revision = '19602cc4f40'
down_revision = '1146bb9cb6ef'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, ForeignKey, Boolean


def upgrade():
    op.add_column('user', Column('auth_user_id', Integer, ForeignKey('auth_user.id')))
    pass


def downgrade():
    op.drop_constraint('user_ibfk_1', 'user', 'foreignkey')
    op.drop_column('user', 'auth_user_id')
    pass
