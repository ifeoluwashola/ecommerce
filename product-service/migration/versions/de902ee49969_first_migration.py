"""First migration

Revision ID: de902ee49969
Revises: 
Create Date: 2024-11-28 20:24:46.863815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de902ee49969'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('product_id', sa.NUMERIC(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('price', sa.FLOAT(), nullable=False),
    sa.Column('category', sa.VARCHAR(), nullable=False),
    sa.Column('stock', sa.INTEGER(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('product_id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###