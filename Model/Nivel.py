from conexao import Db

class Nivel(Db.Model):
    __tablename__ = 'nivel'

    id = Db.Column(Db.Integer, primary_key=True)
    nome = Db.Column(Db.String(50), nullable=False)
    descricao = Db.Column(Db.String(100))

    def __repr__(self):
        return f"<Nivel {self.nome}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
        }
