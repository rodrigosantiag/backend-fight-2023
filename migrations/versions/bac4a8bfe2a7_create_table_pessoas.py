"""create_table_pessoas

Revision ID: bac4a8bfe2a7
Revises:
Create Date: 2024-02-17 15:36:16.932706

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bac4a8bfe2a7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    create_table = """CREATE TABLE IF NOT EXISTS pessoas(
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        apelido VARCHAR(32) NOT NULL UNIQUE,
        nome VARCHAR(100) NOT NULL,
        nascimento DATE NOT NULL,
        stack TEXT
    );"""

    # TODO: create required indexes

    connection = op.get_bind()
    connection.execute(sa.text(create_table))


def downgrade() -> None:
    drop_table = "DROP TABLE IF EXISTS pessoas;"

    connection = op.get_bind()
    connection.execute(sa.text(drop_table))
