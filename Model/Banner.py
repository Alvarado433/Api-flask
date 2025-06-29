from datetime import datetime
from conexao import Db

class Banner(Db.Model):
    __tablename__ = 'banners'

    id = Db.Column(Db.Integer, primary_key=True)
    titulo = Db.Column(Db.String(150), nullable=False)

    # Armazena imagem em binário (longblob)
    imagem_blob = Db.Column(Db.LargeBinary(length=(2**32)-1), nullable=True)

    criado_em = Db.Column(Db.DateTime, default=datetime.utcnow)

    # Chave estrangeira para Oferta
    oferta_id = Db.Column(Db.Integer, Db.ForeignKey('ofertas.id'), nullable=False)

    # Chave estrangeira para Nivel (define se o banner será exibido para o nível)
    nivel_id = Db.Column(Db.Integer, Db.ForeignKey('nivel.id'), nullable=True)

    # Relacionamentos
    oferta = Db.relationship("Oferta", backref=Db.backref("banners", lazy=True))
    nivel = Db.relationship("Nivel", backref=Db.backref("banners", lazy=True))

    def dados(self):
        import base64
        imagem_b64 = base64.b64encode(self.imagem_blob).decode('utf-8') if self.imagem_blob else None

        return {
            "id": self.id,
            "titulo": self.titulo,
            "imagem_blob": imagem_b64,  # envia base64 para frontend
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "oferta_id": self.oferta_id,
            "nivel_id": self.nivel_id,
            "oferta": self.oferta.dados() if self.oferta else None,
            "nivel": self.nivel.to_dict() if self.nivel else None
        }

    def __repr__(self):
        return f"<Banner {self.titulo} - Oferta ID: {self.oferta_id}>"
