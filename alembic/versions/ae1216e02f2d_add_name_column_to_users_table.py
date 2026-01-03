"""Add name column to users table

Revision ID: ae1216e02f2d
Revises: 46b71ed33aef
Create Date: 2026-01-03 12:49:41.056030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae1216e02f2d'
down_revision: Union[str, None] = '46b71ed33aef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'name')
