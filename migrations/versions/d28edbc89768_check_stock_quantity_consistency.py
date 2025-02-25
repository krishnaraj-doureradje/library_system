"""check stock_quantity consistency

Revision ID: d28edbc89768
Revises: ec79d7375721
Create Date: 2025-02-24 22:15:01.268243

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d28edbc89768"
down_revision: Union[str, None] = "ec79d7375721"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("stocks") as batch_op:
        batch_op.create_check_constraint("stock_quantity_check", "stock_quantity >= 0")


def downgrade():
    with op.batch_alter_table("stocks") as batch_op:
        batch_op.drop_constraint("stock_quantity_check", type_="check")
