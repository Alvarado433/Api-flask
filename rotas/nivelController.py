from flask import Blueprint, request, jsonify
from Model.Nivel import Nivel
from conexao import Db


nivel_bp = Blueprint('nivel_bp', __name__, url_prefix='/nivel')

@nivel_bp.route('/listar', methods=['GET'])
def listar_niveis():
    niveis = Nivel.query.all()
    return jsonify([nivel.to_dict() for nivel in niveis]), 200

@nivel_bp.route('/<int:id>', methods=['GET'])
def get_nivel(id):
    nivel = Nivel.query.get_or_404(id)
    return jsonify(nivel.to_dict()), 200

@nivel_bp.route('/', methods=['POST'])
def criar_nivel():
    data = request.get_json()
    nome = data.get('nome')
    descricao = data.get('descricao')

    if not nome:
        return jsonify({"erro": "O campo nome é obrigatório."}), 400

    nivel = Nivel(nome=nome, descricao=descricao)
    Db.session.add(nivel)
    Db.session.commit()

    return jsonify(nivel.to_dict()), 201

@nivel_bp.route('/<int:id>', methods=['PUT'])
def atualizar_nivel(id):
    nivel = Nivel.query.get_or_404(id)
    data = request.get_json()
    nivel.nome = data.get('nome', nivel.nome)
    nivel.descricao = data.get('descricao', nivel.descricao)

    Db.session.commit()
    return jsonify(nivel.to_dict()), 200

@nivel_bp.route('/<int:id>', methods=['DELETE'])
def deletar_nivel(id):
    nivel = Nivel.query.get_or_404(id)
    Db.session.delete(nivel)
    Db.session.commit()
    return jsonify({"mensagem": "Nível deletado com sucesso."}), 200
