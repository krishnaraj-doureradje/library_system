"""Insert reservation statuses

Revision ID: 1f3bc1d32fa5
Revises: 11b5c67d993c
Create Date: 2025-02-22 16:51:14.299379

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1f3bc1d32fa5"
down_revision: Union[str, None] = "11b5c67d993c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO reservation_status (name)
        VALUES
            ('pending'),
            ('confirmed'),
            ('canceled'),
            ('returned');
    """)


def downgrade() -> None:
    op.execute("""
        DELETE FROM reservation_status WHERE name IN ('pending', 'confirmed', 'canceled', 'returned');
    """)
