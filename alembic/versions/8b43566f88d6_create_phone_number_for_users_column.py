"""Create phone number for users column

Revision ID: 8b43566f88d6
Revises: 
Create Date: 2024-04-25 15:27:23.585202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b43566f88d6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable=True))

def downgrade() -> None:
    op.drop_column('users','phone_number')
