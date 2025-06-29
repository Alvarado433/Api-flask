from conexao import Db

class ProdutoOferta(Db.Model):
    __tablename__ = 'produto_oferta'

    id = Db.Column(Db.Integer, primary_key=True)
    produto_id = Db.Column(Db.Integer, Db.ForeignKey('produtos.id'), nullable=False)
    oferta_id = Db.Column(Db.Integer, Db.ForeignKey('ofertas.id'), nullable=False)

    produto = Db.relationship('Produto', back_populates='ofertas_associadas')
    oferta = Db.relationship('Oferta', back_populates='produtos_associados')
    def __repr__(self):
        return f'<ProdutoOferta ProdutoID={self.produto_id} OfertaID={self.oferta_id}>'