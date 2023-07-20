"""age on Employee

Revision ID: 5d66f8d2b0a3
Revises: b58f6b0fdeba
Create Date: 2023-07-20 15:39:25.676562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d66f8d2b0a3'
down_revision = 'b58f6b0fdeba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_employee', sa.Column('age', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_employee', 'age')
    # ### end Alembic commands ###