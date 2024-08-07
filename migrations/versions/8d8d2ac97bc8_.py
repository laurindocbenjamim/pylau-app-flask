"""empty message

Revision ID: 8d8d2ac97bc8
Revises: b5c39e63a46c
Create Date: 2024-07-08 20:01:16.090542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d8d2ac97bc8'
down_revision = 'b5c39e63a46c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('product_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_barcode', sa.String(length=100), nullable=False),
    sa.Column('product_description', sa.String(length=100), nullable=False),
    sa.Column('product_category', sa.String(length=100), nullable=True),
    sa.Column('product_type', sa.String(length=100), nullable=True),
    sa.Column('product_detail', sa.String(length=200), nullable=True),
    sa.Column('product_brand', sa.String(length=55), nullable=True),
    sa.Column('product_measure_unit', sa.String(length=10), nullable=True),
    sa.Column('product_fixed_margin', sa.Double(), nullable=True),
    sa.Column('product_status', sa.Boolean(), nullable=True),
    sa.Column('product_retention_font', sa.String(length=50), nullable=True),
    sa.Column('product_date_added', sa.Date(), nullable=True),
    sa.Column('product_year_added', sa.String(length=4), nullable=True),
    sa.Column('product_month_added', sa.String(length=20), nullable=True),
    sa.Column('product_datetime_added', sa.DateTime(), nullable=True),
    sa.Column('product_date_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('product_id'),
    sa.UniqueConstraint('product_barcode')
    )
    op.drop_table('TEST7')
    op.drop_table('TEST5')
    op.drop_table('TEST')
    op.drop_table('TEST4')
    op.drop_table('TEST3')
    op.drop_table('TEST2')
    op.drop_table('TEST6')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TEST6',
    sa.Column('ID', sa.INTEGER(), nullable=False),
    sa.Column('NAME', sa.TEXT(), nullable=False)
    )
    op.create_table('TEST2',
    sa.Column('ID', sa.INTEGER(), nullable=False),
    sa.Column('NAME', sa.TEXT(), nullable=False)
    )
    op.create_table('TEST3',
    sa.Column('ID', sa.INTEGER(), nullable=False),
    sa.Column('NAME', sa.TEXT(), nullable=False)
    )
    op.create_table('TEST4',
    sa.Column('ID', sa.INTEGER(), nullable=False),
    sa.Column('NAME', sa.TEXT(), nullable=False)
    )
    op.create_table('TEST',
    sa.Column('ID', sa.INTEGER(), nullable=False),
    sa.Column('NAME', sa.TEXT(), nullable=False)
    )
    op.create_table('TEST5',
    sa.Column('ID', sa.INTEGER(), nullable=False),
    sa.Column('NAME', sa.TEXT(), nullable=False)
    )
    op.create_table('TEST7',
    sa.Column('ID', sa.INTEGER(), nullable=False),
    sa.Column('NAME', sa.TEXT(), nullable=False)
    )
    op.drop_table('products')
    # ### end Alembic commands ###
