"""empty message

Revision ID: c88766b08c4c
Revises: 863ee4421e8a
Create Date: 2024-06-17 01:29:42.690313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c88766b08c4c'
down_revision = '863ee4421e8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_user_historic',
    sa.Column('auth_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('device_id', sa.String(length=255), nullable=True),
    sa.Column('is_logged_in', sa.Boolean(), nullable=True),
    sa.Column('date_logged_in', sa.DateTime(), nullable=True),
    sa.Column('date_logged_out', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.userID'], ),
    sa.PrimaryKeyConstraint('auth_id')
    )
    with op.batch_alter_table('user_token', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['token'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_token', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    op.drop_table('auth_user_historic')
    # ### end Alembic commands ###