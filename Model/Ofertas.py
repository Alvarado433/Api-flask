from datetime import datetime
from conexao import Db

class Oferta(Db.Model):
    __tablename__ = 'ofertas'

    id = Db.Column(Db.Integer, primary_key=True)
    titulo = Db.Column(Db.String(150), nullable=False)
    descricao = Db.Column(Db.String(255), nullable=True)
    desconto = Db.Column(Db.Float, nullable=False)
    data_inicio = Db.Column(Db.DateTime, nullable=False, default=datetime.utcnow)
    data_fim = Db.Column(Db.DateTime, nullable=True)

    # Relacionamento direto com Produto (mantido para imagens)
    produto_id = Db.Column(Db.Integer, Db.ForeignKey('produtos.id'), nullable=True)
    produto = Db.relationship('Produto', back_populates='ofertas_heranca', foreign_keys=[produto_id])

    # Relacionamento com a tabela associativa
    produtos_associados = Db.relationship('ProdutoOferta', back_populates='oferta', cascade="all, delete-orphan")

    def dados(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "desconto": self.desconto,
            "data_inicio": self.data_inicio.isoformat() if self.data_inicio else None,
            "data_fim": self.data_fim.isoformat() if self.data_fim else None,
            "produto_id": self.produto_id,
            "produtos": [rel.produto.id for rel in self.produtos_associados]  # lista de IDs
        }

    def __repr__(self):
        return f'<Oferta {self.titulo} - Desconto: {self.desconto}>'
