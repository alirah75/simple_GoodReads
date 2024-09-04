"""create user and blog table migrations

Revision ID: 176c88149a79
Revises: 36be65ed59fb
Create Date: 2024-09-04 02:23:57.443976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '176c88149a79'
down_revision: Union[str, None] = '36be65ed59fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
