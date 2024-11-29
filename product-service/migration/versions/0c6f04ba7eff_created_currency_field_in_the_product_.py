"""Created currency field in the product table

Revision ID: 0c6f04ba7eff
Revises: abf13ac4ccdc
Create Date: 2024-11-29 09:04:14.446202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c6f04ba7eff'
down_revision: Union[str, None] = 'abf13ac4ccdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add `currency` column to `products` table
    op.add_column('products', sa.Column('currency', sa.String(), nullable=False, server_default="USD"))


def downgrade() -> None:
    # Remove `currency` column from `products` table
    op.drop_column('products', 'currency')
