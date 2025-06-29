from flask import Blueprint, request, jsonify

from Model.Categoria import Categoria
from conexao import Db

categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')

# 🔹 Listar todas as categorias
@categoria_bp.route('/listrar', methods=['GET'])
def listar_categorias():
    categorias = Categoria.query.all()
    return jsonify([cat.dados() for cat in categorias]), 200

# 🔹 Buscar uma categoria por ID
@categoria_bp.route('/<int:id>', methods=['GET'])
def obter_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'error': 'Categoria não encontrada.'}), 404
    return jsonify(categoria.dados()), 200

# 🔹 Criar nova categoria
@categoria_bp.route('/cadastrar', methods=['POST'])
def criar_categoria():
    dados = request.json
    nome = dados.get('nome')
    descricao = dados.get('descricao')

    if not nome:
        return jsonify({'error': 'O nome é obrigatório.'}), 400

    if Categoria.query.filter_by(nome=nome).first():
        return jsonify({'error': 'Já existe uma categoria com esse nome.'}), 400

    nova_categoria = Categoria(nome=nome, descricao=descricao)
    Db.session.add(nova_categoria)
    Db.session.commit()

    return jsonify(nova_categoria.dados()), 201

# 🔹 Atualizar categoria existente
@categoria_bp.route('/atualizar/<int:id>', methods=['PUT'])
def atualizar_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'error': 'Categoria não encontrada.'}), 404

    dados = request.json
    categoria.nome = dados.get('nome', categoria.nome)
    categoria.descricao = dados.get('descricao', categoria.descricao)

    Db.session.commit()
    return jsonify(categoria.dados()), 200

# 🔹 Deletar categoria
@categoria_bp.route('/excluir/<int:id>', methods=['DELETE'])
def deletar_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'error': 'Categoria não encontrada.'}), 404

    Db.session.delete(categoria)
    Db.session.commit()
    return jsonify({'message': 'Categoria deletada com sucesso.'}), 200

@categoria_bp.route('/contar', methods=['GET'])
def contar_categorias():
    total = Categoria.query.count()
    return jsonify({'total_categorias': total}), 200
@categoria_bp.route('/nome/<string:nome>', methods=['GET'])
def buscar_por_nome(nome):
    categoria = Categoria.query.filter_by(nome=nome).first()
    if not categoria:
        return jsonify({'error': 'Categoria não encontrada.'}), 404

    produtos = [prod.dados() for prod in categoria.produtos]  # Assumindo que Categoria tem relacionamento produtos
    return jsonify({
        'categoria': categoria.dados(),
        'produtos': produtos
    }), 200
# **ROTA CORRIGIDA PARA FRONTEND**
@categoria_bp.route('/listrar/nome/<string:nome>', methods=['GET'])
def buscar_por_nome_listrar(nome):
    categoria = Categoria.query.filter_by(nome=nome).first()
    if not categoria:
        return jsonify({'error': 'Categoria não encontrada.'}), 404

    produtos = [prod.dados() for prod in categoria.produtos]
    return jsonify({
        'categoria': categoria.dados(),
        'produtos': produtos
    }), 200