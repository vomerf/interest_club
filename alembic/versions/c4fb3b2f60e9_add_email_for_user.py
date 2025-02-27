"""Add email for User

Revision ID: c4fb3b2f60e9
Revises: 006caa028802
Create Date: 2025-01-08 21:35:34.853716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4fb3b2f60e9'
down_revision: Union[str, None] = '006caa028802'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
