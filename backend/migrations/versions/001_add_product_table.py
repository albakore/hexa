"""Add product table for inventory module

Revision ID: 001_product_table
Revises:
Create Date: 2025-11-04

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from decimal import Decimal

# revision identifiers, used by Alembic.
revision = '001_product_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Crea la tabla product para el módulo de inventario
    """
    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sku', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('barcode', sa.String(length=100), nullable=True),
        sa.Column('cost_price', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0.00'),
        sa.Column('sale_price', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0.00'),
        sa.Column('quantity_on_hand', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('quantity_reserved', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('reorder_point', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('reorder_quantity', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('unit_of_measure', sa.String(length=50), nullable=False, server_default='unit'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_stockable', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    # Crear índices para mejorar el rendimiento de búsquedas
    op.create_index('ix_product_sku', 'product', ['sku'], unique=True)
    op.create_index('ix_product_barcode', 'product', ['barcode'], unique=True)
    op.create_index('ix_product_name', 'product', ['name'])
    op.create_index('ix_product_category', 'product', ['category'])
    op.create_index('ix_product_is_active', 'product', ['is_active'])

    # Índice compuesto para búsquedas de productos activos con stock bajo
    op.create_index(
        'ix_product_active_low_stock',
        'product',
        ['is_active', 'quantity_on_hand'],
        postgresql_where=sa.text('is_active = true AND quantity_on_hand <= reorder_point')
    )


def downgrade() -> None:
    """
    Elimina la tabla product y sus índices
    """
    op.drop_index('ix_product_active_low_stock', table_name='product')
    op.drop_index('ix_product_is_active', table_name='product')
    op.drop_index('ix_product_category', table_name='product')
    op.drop_index('ix_product_name', table_name='product')
    op.drop_index('ix_product_barcode', table_name='product')
    op.drop_index('ix_product_sku', table_name='product')
    op.drop_table('product')
