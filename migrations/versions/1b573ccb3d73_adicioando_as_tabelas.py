"""Adicioando as tabelas

Revision ID: 1b573ccb3d73
Revises: 
Create Date: 2025-06-15 00:16:06.443297

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1b573ccb3d73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categoria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('nivel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('descricao', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('produtos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('preco', sa.Float(), nullable=False),
    sa.Column('estoque', sa.String(length=50), nullable=False),
    sa.Column('parcelamento', sa.String(length=100), nullable=True),
    sa.Column('pix_valor', sa.Float(), nullable=True),
    sa.Column('formas_pagamento', sa.String(length=255), nullable=True),
    sa.Column('categoria_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['categoria_id'], ['categoria.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('senha_hash', sa.String(length=255), nullable=False),
    sa.Column('telefone', sa.String(length=20), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('nivel_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['nivel_id'], ['nivel.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email')
    )
    op.create_table('imagem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=True),
    sa.Column('dados_imagem', mysql.LONGBLOB(), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('imagem')
    op.drop_table('usuarios')
    op.drop_table('produtos')
    op.drop_table('nivel')
    op.drop_table('categoria')
    # ### end Alembic commands ###
