"""added clients table

Revision ID: 8c186ff25dd1
Revises: fdf8821871d7
Create Date: 2021-01-07 21:32:09.421998

"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa


revision = '8c186ff25dd1'
down_revision = 'fdf8821871d7'
branch_labels = None
depends_on = None

def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def create_clients_table() -> None:
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("client_id", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("hashed_secret", sa.Text),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_client_modtime
            BEFORE UPDATE
            ON clients
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_clients_table()


def downgrade():
    op.drop_table("clients")
