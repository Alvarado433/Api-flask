from werkzeug.security import generate_password_hash, check_password_hash
from conexao import Db


class Usuario(Db.Model):
    __tablename__ = 'usuarios'

    id = Db.Column(Db.Integer, primary_key=True)
    nome = Db.Column(Db.String(150), nullable=False)
    email = Db.Column(Db.String(150), unique=True, nullable=False)
    senha_hash = Db.Column(Db.String(255), nullable=False)
    telefone = Db.Column(Db.String(20), nullable=False)
    cpf = Db.Column(Db.String(14), unique=True, nullable=False)

    # Relacionamento opcional com nível
    nivel_id = Db.Column(Db.Integer, Db.ForeignKey('nivel.id'), nullable=True)
    nivel = Db.relationship('Nivel', backref='usuarios')

    def __init__(self, nome, email, senha, telefone, cpf, nivel_id=None):
        self.nome = nome
        self.email = email
        self.set_senha(senha)  # gera o hash da senha
        self.telefone = telefone
        self.cpf = cpf
        self.nivel_id = nivel_id

    def set_senha(self, senha: str):
        """Criptografa e armazena a senha, se ela for válida (não vazia e não None)."""
        if senha and senha.strip():
            self.senha_hash = generate_password_hash(senha)
        else:
            # Caso senha seja None ou vazia, não altera a senha_hash
            pass

    def check_senha(self, senha: str) -> bool:
        """Verifica se a senha informada corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    def dados(self) -> dict:
        """Retorna dados do usuário em formato JSON-friendly, omitindo a senha."""
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "cpf": self.cpf,
            "nivel_id": self.nivel_id,
            "nivel": {
                "id": self.nivel.id,
                "nome": self.nivel.nome,
                "descricao": self.nivel.descricao
            } if self.nivel else None
        }

    def __repr__(self):
        return f'<Usuario {self.nome} - {self.email}>'
