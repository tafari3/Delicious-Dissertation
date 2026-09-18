"""scanning and reporting schema"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002_scanning_reporting"
down_revision = "0001_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "scans", sa.Column("endpoint_count", sa.Integer(), nullable=False, server_default="0")
    )
    op.add_column(
        "scans", sa.Column("finding_count", sa.Integer(), nullable=False, server_default="0")
    )
    op.add_column("scans", sa.Column("error_message", sa.Text(), nullable=True))
    op.create_table(
        "findings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "scan_id", sa.Integer(), sa.ForeignKey("scans.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("rule_id", sa.String(80), nullable=False),
        sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("confidence", sa.String(20), nullable=False),
        sa.Column("state", sa.String(30), nullable=False),
        sa.Column("method", sa.String(12), nullable=False, server_default="GET"),
        sa.Column("endpoint", sa.String(1024), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("evidence_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("remediation", sa.Text(), nullable=False, server_default=""),
        sa.Column("owasp", sa.String(120), nullable=True),
        sa.Column("cwe", sa.String(40), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("findings")
    op.drop_column("scans", "error_message")
    op.drop_column("scans", "finding_count")
    op.drop_column("scans", "endpoint_count")
