"""empty message

Revision ID: 790f20a0d684
Revises: 6e6982b4832b
Create Date: 2024-11-25 15:47:06.504659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '790f20a0d684'
down_revision = '6e6982b4832b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_payment_link', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.drop_column('course_payment_link')

    # ### end Alembic commands ###
