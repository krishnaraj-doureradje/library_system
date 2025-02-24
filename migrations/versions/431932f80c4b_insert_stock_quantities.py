"""Insert stock quantities

Revision ID: 431932f80c4b
Revises: c62c6444afe9
Create Date: 2025-02-22 17:12:46.139816

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "431932f80c4b"
down_revision: Union[str, None] = "c62c6444afe9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO stocks (book_id, stock_quantity, created_at, updated_at)
        VALUES
            (1, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            (2, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            (3, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            (4, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            (5, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    """)


def downgrade() -> None:
    op.execute("""
        DELETE FROM stocks WHERE book_id IN (1, 2, 3, 4, 5);
    """)
