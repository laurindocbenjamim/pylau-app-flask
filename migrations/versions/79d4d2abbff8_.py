"""empty message

Revision ID: 79d4d2abbff8
Revises: 760c8553e57d
Create Date: 2024-06-05 12:53:10.084340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79d4d2abbff8'
down_revision = '760c8553e57d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('_token', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userID', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('_token', schema=None) as batch_op:
        batch_op.drop_column('userID')

    # ### end Alembic commands ###
