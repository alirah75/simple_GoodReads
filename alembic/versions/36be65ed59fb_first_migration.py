"""first migration

Revision ID: 36be65ed59fb
Revises: 771bc1f82ef4
Create Date: 2024-09-04 02:23:36.903020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36be65ed59fb'
down_revision: Union[str, None] = '771bc1f82ef4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
