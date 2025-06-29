from typing import Dict, Any
from conexao import Db
import base64
from sqlalchemy.dialects.mysql import LONGBLOB
class Imagem(Db.Model):
    __tablename__ = 'imagem'

    id = Db.Column(Db.Integer, primary_key=True)
    produto_id = Db.Column(Db.Integer, Db.ForeignKey('produtos.id'), nullable=True)
    dados_imagem = Db.Column(LONGBLOB, nullable=False)
    descricao = Db.Column(Db.String(255), nullable=True)

    produto = Db.relationship('Produto', back_populates='imagens')
    miniatura = Db.relationship('Miniatura', back_populates='imagem', uselist=False, cascade="all, delete-orphan")

    def dados(self) -> Dict[str, Any]:
        imagem_base64 = base64.b64encode(self.dados_imagem).decode('utf-8') if self.dados_imagem else None
        miniatura_base64 = self.miniatura.dados_base64() if self.miniatura else None
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "descricao": self.descricao,
            "imagem_base64": imagem_base64,
            "miniatura_base64": miniatura_base64,
        }

class Miniatura(Db.Model):
    __tablename__ = 'miniatura'

    id = Db.Column(Db.Integer, primary_key=True)
    imagem_id = Db.Column(Db.Integer, Db.ForeignKey('imagem.id'), nullable=False, unique=True)
    dados_miniatura = Db.Column(Db.LargeBinary, nullable=False)  # miniatura da imagem

    imagem = Db.relationship('Imagem', back_populates='miniatura')

    def dados_base64(self) -> str:
        return base64.b64encode(self.dados_miniatura).decode('utf-8') if self.dados_miniatura else None
