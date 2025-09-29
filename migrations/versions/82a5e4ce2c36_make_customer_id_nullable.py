"""Make customer_id nullable

Revision ID: 82a5e4ce2c36
Revises: 4e4c21b5e6ee
Create Date: 2025-09-29 18:07:24.431932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82a5e4ce2c36'
down_revision = '4e4c21b5e6ee'
branch_labels = None
depends_on = None



def upgrade():
    op.alter_column(
        'orders',
        'customer_id',
        existing_type=sa.Integer(),
        nullable=True
    )

def downgrade():
    op.alter_column(
        'orders',
        'customer_id',
        existing_type=sa.Integer(),
        nullable=False
    )