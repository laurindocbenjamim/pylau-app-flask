"""empty message

Revision ID: 9f958920eefc
Revises: 43ce86a23fa9
Create Date: 2024-05-31 18:19:10.044850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f958920eefc'
down_revision = '43ce86a23fa9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('two_factor_auth_secret', sa.String(length=200), nullable=False))
        batch_op.drop_column('two_factor_auth_code')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('two_factor_auth_code', sa.VARCHAR(length=10), nullable=True))
        batch_op.drop_column('two_factor_auth_secret')

    # ### end Alembic commands ###
