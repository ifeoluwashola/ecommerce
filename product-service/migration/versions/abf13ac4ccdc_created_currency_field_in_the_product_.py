"""Created currency field in the product table

Revision ID: abf13ac4ccdc
Revises: a9b65f43a617
Create Date: 2024-11-29 08:39:34.687686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abf13ac4ccdc'
down_revision: Union[str, None] = 'a9b65f43a617'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add `currency` column to `products` table
    op.add_column('products', sa.Column('currency', sa.String(), nullable=False, server_default="USD"))


def downgrade() -> None:
    # Remove `currency` column from `products` table
    op.drop_column('products', 'currency')
