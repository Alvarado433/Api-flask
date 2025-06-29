from datetime import datetime
from conexao import Db

class Pedido(Db.Model):
    __tablename__ = "pedidos"

    id = Db.Column(Db.Integer, primary_key=True)
    usuario_id = Db.Column(Db.Integer, Db.ForeignKey("usuarios.id"), nullable=False)
    nome_completo = Db.Column(Db.String(150), nullable=False)
    cpf = Db.Column(Db.String(14), nullable=False)
    telefone = Db.Column(Db.String(20), nullable=False)
    email = Db.Column(Db.String(120), nullable=False)
    cep = Db.Column(Db.String(9), nullable=False)
    endereco = Db.Column(Db.String(200), nullable=False)
    numero = Db.Column(Db.String(20), nullable=False)
    complemento = Db.Column(Db.String(100), nullable=True)
    bairro = Db.Column(Db.String(100), nullable=False)
    cidade = Db.Column(Db.String(100), nullable=False)
    estado = Db.Column(Db.String(2), nullable=False)
    valor_total = Db.Column(Db.Float, nullable=False)
    status = Db.Column(Db.String(50), default="pendente")
    data_criacao = Db.Column(Db.DateTime, default=datetime.utcnow)

    usuario = Db.relationship("Usuario", backref="pedidos")
    itens = Db.relationship("PedidoItem", backref="pedido", lazy=True)

class PedidoItem(Db.Model):
    __tablename__ = "pedido_item"

    id = Db.Column(Db.Integer, primary_key=True)
    pedido_id = Db.Column(Db.Integer, Db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = Db.Column(Db.Integer, Db.ForeignKey("produtos.id"), nullable=False)
    quantidade = Db.Column(Db.Integer, nullable=False, default=1)
    preco_unitario = Db.Column(Db.Float, nullable=False)

    produto = Db.relationship("Produto", backref="pedido_itens")
