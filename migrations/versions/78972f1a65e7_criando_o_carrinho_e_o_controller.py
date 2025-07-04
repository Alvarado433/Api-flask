"""Criando o carrinho  e o controller

Revision ID: 78972f1a65e7
Revises: a490d5dd7894
Create Date: 2025-06-23 13:12:35.786744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '78972f1a65e7'
down_revision = 'a490d5dd7894'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carrinho_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('banners', schema=None) as batch_op:
        batch_op.alter_column('imagem_blob',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=4294967295),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('banners', schema=None) as batch_op:
        batch_op.alter_column('imagem_blob',
               existing_type=sa.LargeBinary(length=4294967295),
               type_=mysql.LONGBLOB(),
               existing_nullable=True)

    op.drop_table('carrinho_item')
    # ### end Alembic commands ###
