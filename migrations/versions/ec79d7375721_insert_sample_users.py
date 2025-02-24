"""Insert sample users

Revision ID: ec79d7375721
Revises: 431932f80c4b
Create Date: 2025-02-22 17:18:27.588289

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ec79d7375721"
down_revision: Union[str, None] = "431932f80c4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO users (first_name, last_name, email, created_at, updated_at)
        VALUES 
            ('John', 'Doe', 'john.doe@example.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            ('Jane', 'Smith', 'jane.smith@example.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            ('Alice', 'Johnson', 'alice.johnson@example.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            ('Bob', 'Brown', 'bob.brown@example.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            ('Charlie', 'Davis', 'charlie.davis@example.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    """)


def downgrade() -> None:
    op.execute("""
        DELETE FROM users WHERE email IN (
            'john.doe@example.com',
            'jane.smith@example.com',
            'alice.johnson@example.com',
            'bob.brown@example.com',
            'charlie.davis@example.com'
        );
    """)
