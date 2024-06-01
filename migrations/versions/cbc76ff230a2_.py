"""empty message

Revision ID: cbc76ff230a2
Revises: 2244d76c75ca
Create Date: 2024-06-01 12:49:28.950881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbc76ff230a2'
down_revision = '2244d76c75ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('softcartDimCountry')
    op.drop_table('softcartDimCategory')
    op.drop_table('softcartFactSales')
    op.drop_table('softcartDimItem')
    op.drop_table('softcartDimDate')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('softcartDimDate',
    sa.Column('dateid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('month', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('monthName', sa.CHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('day', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('dayOfWeek', sa.CHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quarter ', sa.String(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('dateid', name='softcartDimDate_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('softcartDimItem',
    sa.Column('itemid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('item', sa.CHAR(length=1), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('itemid', name='softcartDimItem_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('softcartFactSales',
    sa.Column('salesid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('itemid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('categoryid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('countryid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('dateid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('price', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['categoryid'], ['softcartDimCategory.categoryid'], name='categoryitem'),
    sa.ForeignKeyConstraint(['countryid'], ['softcartDimCountry.countryid'], name='countrysales'),
    sa.ForeignKeyConstraint(['dateid'], ['softcartDimDate.dateid'], name='datesales'),
    sa.ForeignKeyConstraint(['itemid'], ['softcartDimItem.itemid'], name='itemsales'),
    sa.PrimaryKeyConstraint('salesid', name='softcartFactSales_pkey')
    )
    op.create_table('softcartDimCategory',
    sa.Column('categoryid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('category', sa.CHAR(length=1), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('categoryid', name='softcartDimCategory_pkey')
    )
    op.create_table('softcartDimCountry',
    sa.Column('countryid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('country', sa.CHAR(length=1), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('countryid', name='softcartDimCountry_pkey')
    )
    # ### end Alembic commands ###
