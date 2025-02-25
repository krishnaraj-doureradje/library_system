from sqlalchemy import Delete, delete
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.models.author import Author


def get_author_stmt(author_id: int) -> SelectOfScalar[Author]:
    """This function returns a select statement to get the Author.

    Args:
        author_id (int): The author id

    Returns:
        SelectOfScalar[Author]: Select statement for author.
    """
    stmt = select(Author).where(Author.id == author_id)
    return stmt


def delete_author_from_id_stmt(author_id: int) -> Delete:
    """This function return delete author statement

    Args:
        author_id (int): Author id to be deleted

    Returns:
         Delete: Delete statement
    """
    stmt = delete(Author).where(Author.id == author_id)  # type: ignore
    return stmt
