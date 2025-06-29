from conexao import Db


class Cupom(Db.Model):
    __tablename__ = 'cupoms'

    id = Db.Column(Db.Integer, primary_key=True)
    codigo = Db.Column(Db.String(20), unique=True, nullable=False)
    min_price = Db.Column(Db.Float, nullable=False)
    max_price = Db.Column(Db.Float, nullable=True)
    desconto = Db.Column(Db.Float, nullable=True)
    frete_gratis = Db.Column(Db.Boolean, default=False)
    descricao = Db.Column(Db.String(255), nullable=True)
    status_id = Db.Column(Db.Integer, Db.ForeignKey('nivel.id'), nullable=False)
    validade = Db.Column(Db.Date, nullable=True)  # opcional

    nivel = Db.relationship('Nivel', backref='cupons')

    def Dados(self):
        return {
            "codigo": self.codigo,
            "minPrice": self.min_price,
            "maxPrice": self.max_price,
            "discount": self.desconto,
            "freeShipping": self.frete_gratis,
            "label": self.descricao,
            "statusId": self.status_id,
            "statusNome": self.nivel.nome if self.nivel else None,
            "validade": self.validade.isoformat() if self.validade else None
        }
