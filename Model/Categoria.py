from typing import Dict, Any
from conexao import Db

class Categoria(Db.Model):
    __tablename__ = 'categoria'

    id = Db.Column(Db.Integer, primary_key=True)
    nome = Db.Column(Db.String(100), unique=True, nullable=False)
    descricao = Db.Column(Db.String(255), nullable=True)

    produtos = Db.relationship(
        'Produto',
        back_populates='categoria',
        lazy=True
    )

    def dados(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'produtos': [produto.dados() for produto in self.produtos]
        }
