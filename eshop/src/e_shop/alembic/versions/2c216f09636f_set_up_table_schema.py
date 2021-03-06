"""set up table schema

Revision ID: 2c216f09636f
Revises: 
Create Date: 2015-04-12 22:13:19.060479

"""

# revision identifiers, used by Alembic.
revision = '2c216f09636f'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.Column('company_name', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('upload_file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.Column('path', sa.String(length=200, convert_unicode=True), nullable=True),
    sa.Column('format', sa.String(length=10, convert_unicode=True), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.Column('mobile', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.Column('tel', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.Column('address', sa.String(length=200, convert_unicode=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('brand_upload_file',
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['file_id'], ['upload_file.id'], )
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('parent_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_upload_file',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['upload_file.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('commodity_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commodity_custom_field',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('field_name', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.Column('field_type', sa.Integer(), nullable=True),
    sa.Column('meta_id', sa.Integer(), nullable=True),
    sa.Column('note', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['meta_id'], ['commodity_meta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commodity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50, convert_unicode=True), nullable=True),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('base_price', sa.DECIMAL(), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('meta_id', sa.Integer(), nullable=True),
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['meta_id'], ['commodity_meta.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commodity_id', sa.Integer(), nullable=True),
    sa.Column('discount', sa.DECIMAL(), nullable=True),
    sa.Column('note', sa.Unicode(length=50), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('is_all_applied', sa.Boolean(), nullable=True),
    sa.Column('name', sa.Unicode(length=50), nullable=True),
    sa.Column('limit_per_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['commodity_id'], ['commodity.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commodity_upload_file',
    sa.Column('commodity_id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['commodity_id'], ['commodity.id'], ),
    sa.ForeignKeyConstraint(['file_id'], ['upload_file.id'], ),
    sa.PrimaryKeyConstraint('commodity_id', 'file_id')
    )
    op.create_table('commodity_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commodity_id', sa.Integer(), nullable=True),
    sa.Column('custom_field_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Unicode(length=50), nullable=True),
    sa.ForeignKeyConstraint(['commodity_id'], ['commodity.id'], ),
    sa.ForeignKeyConstraint(['custom_field_id'], ['commodity_custom_field.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_addr', sa.String(length=50), nullable=True),
    sa.Column('note', sa.UnicodeText(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('commodity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['commodity_id'], ['commodity.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discount_commodity',
    sa.Column('discount_id', sa.Integer(), nullable=True),
    sa.Column('commodity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['commodity_id'], ['commodity.id'], ),
    sa.ForeignKeyConstraint(['discount_id'], ['discount.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('discount_commodity')
    op.drop_table('comment')
    op.drop_table('commodity_detail')
    op.drop_table('commodity_upload_file')
    op.drop_table('discount')
    op.drop_table('commodity')
    op.drop_table('commodity_custom_field')
    op.drop_table('commodity_meta')
    op.drop_table('user_upload_file')
    op.drop_table('category')
    op.drop_table('brand_upload_file')
    op.drop_table('user')
    op.drop_table('upload_file')
    op.drop_table('brand')
    ### end Alembic commands ###
