"""Atu

Revision ID: 694a6905fd0d
Revises: 77a4c169092e
Create Date: 2025-06-17 00:06:43.515935

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '694a6905fd0d'
down_revision = '77a4c169092e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('produto_oferta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=False),
    sa.Column('oferta_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['oferta_id'], ['ofertas.id'], ),
    sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('banners', schema=None) as batch_op:
        batch_op.alter_column('imagem_blob',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=4294967295),
               existing_nullable=True)

    with op.batch_alter_table('ofertas', schema=None) as batch_op:
        batch_op.alter_column('produto_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ofertas', schema=None) as batch_op:
        batch_op.alter_column('produto_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    with op.batch_alter_table('banners', schema=None) as batch_op:
        batch_op.alter_column('imagem_blob',
               existing_type=sa.LargeBinary(length=4294967295),
               type_=mysql.LONGBLOB(),
               existing_nullable=True)

    op.drop_table('produto_oferta')
    # ### end Alembic commands ###
