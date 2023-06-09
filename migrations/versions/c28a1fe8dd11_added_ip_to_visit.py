"""added ip to visit

Revision ID: c28a1fe8dd11
Revises: a08ae3239cbf
Create Date: 2023-05-14 15:25:12.041455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c28a1fe8dd11'
down_revision = 'a08ae3239cbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visit', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visitor_ip', sa.String(length=15), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visit', schema=None) as batch_op:
        batch_op.drop_column('visitor_ip')

    # ### end Alembic commands ###
