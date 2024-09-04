"""finally changeing in app

Revision ID: afe6596d435f
Revises: 176c88149a79
Create Date: 2024-09-05 03:17:31.996395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afe6596d435f'
down_revision: Union[str, None] = '176c88149a79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
