from conexao import Db

class CarrinhoItem(Db.Model):
    __tablename__ = "carrinho_item"

    id = Db.Column(Db.Integer, primary_key=True)
    produto_id = Db.Column(Db.Integer, Db.ForeignKey("produtos.id"), nullable=False)
    usuario_id = Db.Column(Db.Integer, Db.ForeignKey("usuarios.id"), nullable=False)
    quantidade = Db.Column(Db.Integer, nullable=False, default=1)

    produto = Db.relationship("Produto", backref="carrinho_items")
    usuario = Db.relationship("Usuario", backref="carrinho_items")

    def dados(self):
        return {
            "id": self.id,
            "produto": self.produto.dados() if self.produto else None,
            "quantidade": self.quantidade,
            "usuario_id": self.usuario_id
        }
