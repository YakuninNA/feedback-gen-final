"""TESTDB14

Revision ID: 773eab6535f6
Revises: 2f0f7db982de
Create Date: 2024-10-20 01:42:59.213063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '773eab6535f6'
down_revision: Union[str, None] = '2f0f7db982de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert roles into the roles table
    op.execute(
        """
        INSERT INTO roles (id, role_name) VALUES
        (0, 'ADMIN'),
        (1, 'INTERVIEWER')
        """
    )


def downgrade() -> None:
    # Remove the roles that were inserted
    op.execute(
        """
        DELETE FROM roles WHERE id IN (0, 1)
        """
    )
