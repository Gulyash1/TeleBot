"""init schema

Revision ID: d7dd274d1fc6
Revises: 
Create Date: 2025-09-16 22:11:05.444701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7dd274d1fc6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema with SQLite-safe operations.
    - If table 'maintance' doesn't exist: create it with id PK.
    - If exists but has no 'id': recreate and copy data.
    - If already has 'id': do nothing.
    """
    bind = op.get_bind()
    insp = sa.inspect(bind)
    tables = set(insp.get_table_names())

    if 'maintance' not in tables:
        op.create_table(
            'maintance',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
            sa.Column('date', sa.Date(), nullable=False),
            sa.Column('mileage', sa.Integer()),
            sa.Column('description', sa.String()),
        )
        return

    cols = {c['name'] for c in insp.get_columns('maintance')}
    if 'id' in cols:
        # Already migrated
        return

    # Recreate table to add NOT NULL PK column
    op.create_table(
        'maintance_new',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('mileage', sa.Integer()),
        sa.Column('description', sa.String()),
    )
    op.execute(
        "INSERT INTO maintance_new (date, mileage, description) "
        "SELECT date, mileage, description FROM maintance"
    )
    op.drop_table('maintance')
    op.rename_table('maintance_new', 'maintance')


def downgrade() -> None:
    """Downgrade schema: best-effort recreate without id PK if present."""
    bind = op.get_bind()
    insp = sa.inspect(bind)
    tables = set(insp.get_table_names())

    if 'maintance' not in tables:
        return

    cols = {c['name'] for c in insp.get_columns('maintance')}
    if 'id' not in cols:
        return

    op.create_table(
        'maintance_old',
        sa.Column('date', sa.Date(), primary_key=True, nullable=False),
        sa.Column('mileage', sa.Integer()),
        sa.Column('description', sa.String()),
    )
    op.execute(
        "INSERT INTO maintance_old (date, mileage, description) "
        "SELECT date, mileage, description FROM maintance"
    )
    op.drop_table('maintance')
    op.rename_table('maintance_old', 'maintance')
