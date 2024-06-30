"""empty message

Revision ID: 3d3ced1ba6ec
Revises: bfb05d91882e
Create Date: 2024-06-29 17:57:00.759749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d3ced1ba6ec'
down_revision = 'bfb05d91882e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth_user_historic', schema=None) as batch_op:
        batch_op.alter_column('date_logged_in',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    with op.batch_alter_table('two_fa_auth', schema=None) as batch_op:
        batch_op.add_column(sa.Column('datetime_added', sa.DateTime(), nullable=True))
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    with op.batch_alter_table('user_token', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('datetime_added', sa.DateTime(), nullable=True))
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)
        batch_op.drop_column('datetime_added')

    with op.batch_alter_table('user_token', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    with op.batch_alter_table('two_fa_auth', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)
        batch_op.drop_column('datetime_added')

    with op.batch_alter_table('auth_user_historic', schema=None) as batch_op:
        batch_op.alter_column('date_logged_in',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###