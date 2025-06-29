from conexao import Db

class Produto(Db.Model):
    __tablename__ = 'produtos'

    id = Db.Column(Db.Integer, primary_key=True)
    nome = Db.Column(Db.String(150), nullable=False)
    preco = Db.Column(Db.Float, nullable=False)
    estoque = Db.Column(Db.String(50), nullable=False)
    parcelamento = Db.Column(Db.String(100), nullable=True)
    pix_valor = Db.Column(Db.Float, nullable=True)
    formas_pagamento = Db.Column(Db.String(255), nullable=True)

    categoria_id = Db.Column(Db.Integer, Db.ForeignKey('categoria.id'), nullable=False)
    categoria = Db.relationship('Categoria', back_populates='produtos')

    imagens = Db.relationship('Imagem', back_populates='produto', lazy=True, cascade="all, delete-orphan")

    # Relacionamento original (herança direta)
    ofertas_heranca = Db.relationship('Oferta', back_populates='produto')

    # Relacionamento via tabela associativa
    ofertas_associadas = Db.relationship('ProdutoOferta', back_populates='produto', cascade="all, delete-orphan")

    def dados(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "estoque": self.estoque,
            "parcelamento": self.parcelamento,
            "pix_valor": self.pix_valor,
            "formas_pagamento": self.formas_pagamento.split(",") if self.formas_pagamento else [],
            "categoria": {
                "id": self.categoria.id,
                "nome": self.categoria.nome,
            } if self.categoria else None,
            "imagens": [img.dados() for img in self.imagens] if self.imagens else [],
            "ofertas": [rel.oferta.dados() for rel in self.ofertas_associadas] if self.ofertas_associadas else []
        }

    def __repr__(self):
        return f'<Produto {self.nome} - R${self.preco:.2f}>'
