"""Insert books details

Revision ID: c62c6444afe9
Revises: 0182dd89602f
Create Date: 2025-02-22 17:09:32.120398

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c62c6444afe9"
down_revision: Union[str, None] = "0182dd89602f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        INSERT INTO books (title, author_id, published_date, category, created_at, updated_at)
        VALUES
            ('The Pragmatic Programmer', 1, '1999-10-30', 'Programming', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            ('Clean Code', 2, '2008-08-01', 'Programming', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            ('The Great Gatsby', 3, '1925-04-10', 'Literature', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            ('The Theory of Everything', 4, '2002-01-01', 'Science', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            ('The Metamorphosis', 5, '1915-10-01', 'Literature', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    """)


def downgrade():
    op.execute("""
        DELETE FROM books WHERE title IN (
            'The Pragmatic Programmer',
            'Clean Code',
            'The Great Gatsby',
            'The Theory of Everything',
            'The Metamorphosis'
        );
    """)
