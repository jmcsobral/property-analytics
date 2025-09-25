"""add interesting to annotations

Revision ID: 8c0f15e630ed
Revises: ef6657ece334
Create Date: 2025-09-15 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "945cdf2212a9"
down_revision = "303aaf230fcc"   # <-- set parent to your baseline (current head)
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        "annotations",
        sa.Column("interesting", sa.String(length=10), nullable=True),
    )
    op.create_index(
        "ix_annotations_interesting",
        "annotations",
        ["interesting"],
    )


def downgrade():
    op.drop_index("ix_annotations_interesting", table_name="annotations")
    op.drop_column("annotations", "interesting")
