"""Create admin_users, authors, books, reservations, reservation_status and users tables

Revision ID: 11b5c67d993c
Revises:
Create Date: 2025-02-22 16:46:03.385968

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "11b5c67d993c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admin_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column("password", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_admin_users_user_id"), "admin_users", ["user_id"], unique=True)
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("last_name", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.Column("nationality", sqlmodel.sql.sqltypes.AutoString(length=3), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "first_name", "last_name", "birth_date", name="uq_author_name_birthdate"
        ),
    )
    op.create_index(op.f("ix_authors_first_name"), "authors", ["first_name"], unique=False)
    op.create_index(op.f("ix_authors_id"), "authors", ["id"], unique=False)
    op.create_index(op.f("ix_authors_last_name"), "authors", ["last_name"], unique=False)
    op.create_table(
        "reservation_status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_reservation_status_id"), "reservation_status", ["id"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("last_name", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_first_name"), "users", ["first_name"], unique=False)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_last_name"), "users", ["last_name"], unique=False)
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("published_date", sa.Date(), nullable=False),
        sa.Column("category", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "title", "author_id", "published_date", name="uq_title_authorid_publish_date"
        ),
    )
    op.create_index(op.f("ix_books_author_id"), "books", ["author_id"], unique=False)
    op.create_index(op.f("ix_books_id"), "books", ["id"], unique=False)
    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column(
            "borrowed_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("due_date", sa.DateTime(), nullable=False),
        sa.Column("returned_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["books.id"],
        ),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["reservation_status.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reservations_book_id"), "reservations", ["book_id"], unique=False)
    op.create_index(op.f("ix_reservations_id"), "reservations", ["id"], unique=False)
    op.create_index(op.f("ix_reservations_user_id"), "reservations", ["user_id"], unique=False)
    op.create_table(
        "stocks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("stock_quantity", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["books.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stocks_book_id"), "stocks", ["book_id"], unique=True)
    op.create_index(op.f("ix_stocks_id"), "stocks", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_stocks_id"), table_name="stocks")
    op.drop_index(op.f("ix_stocks_book_id"), table_name="stocks")
    op.drop_table("stocks")
    op.drop_index(op.f("ix_reservations_user_id"), table_name="reservations")
    op.drop_index(op.f("ix_reservations_id"), table_name="reservations")
    op.drop_index(op.f("ix_reservations_book_id"), table_name="reservations")
    op.drop_table("reservations")
    op.drop_index(op.f("ix_books_id"), table_name="books")
    op.drop_index(op.f("ix_books_author_id"), table_name="books")
    op.drop_table("books")
    op.drop_index(op.f("ix_users_last_name"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_first_name"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_reservation_status_id"), table_name="reservation_status")
    op.drop_table("reservation_status")
    op.drop_index(op.f("ix_authors_last_name"), table_name="authors")
    op.drop_index(op.f("ix_authors_id"), table_name="authors")
    op.drop_index(op.f("ix_authors_first_name"), table_name="authors")
    op.drop_table("authors")
    op.drop_index(op.f("ix_admin_users_user_id"), table_name="admin_users")
    op.drop_table("admin_users")
