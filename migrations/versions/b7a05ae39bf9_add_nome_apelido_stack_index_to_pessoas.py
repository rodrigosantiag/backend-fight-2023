"""add_nome_apelido_stack_index_to_pessoas

Revision ID: b7a05ae39bf9
Revises: bac4a8bfe2a7
Create Date: 2024-04-27 07:30:19.893172

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7a05ae39bf9"
down_revision: Union[str, None] = "bac4a8bfe2a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = """CREATE EXTENSION IF NOT EXISTS pg_trgm;

            CREATE INDEX IF NOT EXISTS idx_nome_apelido_stack_trgm
            ON pessoas USING gin (nome gin_trgm_ops, apelido gin_trgm_ops, stack gin_trgm_ops);
          """

    connection = op.get_bind()
    connection.execute(sa.text(sql))


def downgrade() -> None:
    sql = "DROP INDEX IF EXISTS idx_nome_apelido_stack_trgm;"

    connection = op.get_bind()
    connection.execute(sa.text(sql))
