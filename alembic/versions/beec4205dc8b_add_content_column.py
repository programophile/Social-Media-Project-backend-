""" add content column

Revision ID: beec4205dc8b
Revises: f01304e5fd80
Create Date: 2026-08-18 15:00:43.935227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'beec4205dc8b'
down_revision: Union[str, Sequence[str], None] = 'f01304e5fd80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
