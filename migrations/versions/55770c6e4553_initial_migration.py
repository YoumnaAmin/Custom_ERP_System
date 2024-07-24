"""Initial migration

Revision ID: 55770c6e4553
Revises: 
Create Date: 2024-07-17 02:03:09.259673

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the desired schema
    op.create_table(
        'order_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('client_id', sa.Integer, nullable=False),
        sa.Column('order', sa.String, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('date', sa.DateTime, nullable=False, server_default=func.now()),
        # Add other columns as needed
    )

    # Copy data from the old table to the new table
    op.execute('INSERT INTO order_new (id, client_id, order, quantity) SELECT id, client_id, order, quantity FROM "order"')

    # Drop the old table if it exists
    op.drop_table('order')

    # Rename the new table to the original table name
    op.rename_table('order_new', 'order')

def downgrade():
    # Create the original table
    op.create_table('order',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('client_id', sa.Integer, nullable=False),
        sa.Column('order', sa.String, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Drop the new table
    op.drop_table('order')
