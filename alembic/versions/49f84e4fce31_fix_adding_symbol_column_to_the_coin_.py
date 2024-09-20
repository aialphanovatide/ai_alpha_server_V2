"""fix: adding symbol column to the coin schema

Revision ID: 49f84e4fce31
Revises: 2a9252ae02f4
Create Date: 2024-09-18 19:03:03.353085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '49f84e4fce31'
down_revision: Union[str, None] = '2a9252ae02f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('coin_bot')]

    if 'symbol' not in existing_columns:
        op.add_column('coin_bot', sa.Column('symbol', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('coin_bot')]

    if 'symbol' in existing_columns:
        op.drop_column('coin_bot', 'symbol')
    # ### end Alembic commands ###