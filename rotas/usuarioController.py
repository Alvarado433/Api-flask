from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from Model.Usuario import Usuario
from conexao import Db


usuario_bp = Blueprint('usuario_bp', __name__)

# Criar usuário
@usuario_bp.route('/usuarios/cadastrar', methods=['POST'])
def criar_usuario():
    data = request.json
    if not data:
        return jsonify({"erro": "Dados não enviados"}), 400
    
    # Validação simples (pode ser expandida)
    required = ['nome', 'email', 'senha', 'telefone', 'cpf']
    if not all(field in data for field in required):
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400

    # Verifica se email ou cpf já existem
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"erro": "Email já cadastrado"}), 400
    if Usuario.query.filter_by(cpf=data['cpf']).first():
        return jsonify({"erro": "CPF já cadastrado"}), 400

    novo_usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        senha=data['senha'],
        telefone=data['telefone'],
        cpf=data['cpf'],
        nivel_id = data.get('nivel_id', 1)  # Usa 1 como padrão (cliente) se não vier nada
 # opcional
    )
    Db.session.add(novo_usuario)
    Db.session.commit()
    return jsonify({"mensagem": "Usuário criado com sucesso", "usuario": novo_usuario.dados()}), 201

# Listar todos os usuários
@usuario_bp.route('/usuarios/Listrar', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.dados() for u in usuarios])

# Buscar usuário por ID
@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify(usuario.dados())

# Atualizar usuário
@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json
    if not data:
        return jsonify({"erro": "Dados não enviados"}), 400

    usuario.nome = data.get('nome', usuario.nome)
    usuario.email = data.get('email', usuario.email)
    if 'senha' in data:
        usuario.set_senha(data['senha'])
    usuario.telefone = data.get('telefone', usuario.telefone)
    usuario.cpf = data.get('cpf', usuario.cpf)
    usuario.nivel_id = data.get('nivel_id', usuario.nivel_id)

    Db.session.commit()
    return jsonify({"mensagem": "Usuário atualizado", "usuario": usuario.dados()})

# Deletar usuário
@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    Db.session.delete(usuario)
    Db.session.commit()
    return jsonify({"mensagem": "Usuário deletado"})

