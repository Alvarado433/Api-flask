from flask import Blueprint, request, jsonify
from datetime import datetime
from conexao import Db

from Model.Ofertas import Oferta
from Model.Produto import Produto
from Model.ProdutoOferta import ProdutoOferta  # Tabela associativa

oferta_bp = Blueprint('oferta', __name__, url_prefix='/ofertas')


# 🔹 Listar todas as ofertas
@oferta_bp.route('/listrar', methods=['GET'])
def listar_ofertas():
    ofertas = Oferta.query.all()
    return jsonify([oferta.dados() for oferta in ofertas]), 200


# 🔹 Buscar oferta por ID
@oferta_bp.route('/<int:id>', methods=['GET'])
def obter_oferta(id):
    oferta = Oferta.query.get(id)
    if not oferta:
        return jsonify({'error': 'Oferta não encontrada.'}), 404
    return jsonify(oferta.dados()), 200


# 🔹 Criar nova oferta com múltiplos produtos
@oferta_bp.route('/cadastrar', methods=['POST'])
def criar_oferta():
    dados = request.json
    titulo = dados.get('titulo')
    desconto = dados.get('desconto')
    produto_id = dados.get('produto_id')  # Produto principal (para imagem, etc)
    produtos_ids = dados.get('produtos_ids', [])  # Produtos adicionais relacionados

    if not titulo or desconto is None or not produto_id:
        return jsonify({'error': 'Título, desconto e produto_id são obrigatórios.'}), 400

    produto_principal = Produto.query.get(produto_id)
    if not produto_principal:
        return jsonify({'error': 'Produto principal não encontrado.'}), 404

    descricao = dados.get('descricao')
    data_inicio_str = dados.get('data_inicio')
    data_fim_str = dados.get('data_fim')

    try:
        data_inicio = datetime.fromisoformat(data_inicio_str) if data_inicio_str else datetime.utcnow()
        data_fim = datetime.fromisoformat(data_fim_str) if data_fim_str else None
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use ISO 8601.'}), 400

    nova_oferta = Oferta(
        titulo=titulo,
        descricao=descricao,
        desconto=desconto,
        data_inicio=data_inicio,
        data_fim=data_fim,
        produto_id=produto_id  # relação direta (exibição principal, imagem, etc)
    )

    Db.session.add(nova_oferta)
    Db.session.flush()  # Garantir ID da oferta antes das associações

    # 🔗 Relacionar produtos adicionais
    for pid in produtos_ids:
        produto = Produto.query.get(pid)
        if produto:
            relacao = ProdutoOferta(produto_id=pid, oferta_id=nova_oferta.id)
            Db.session.add(relacao)

    Db.session.commit()
    return jsonify(nova_oferta.dados()), 201


# 🔹 Atualizar uma oferta
@oferta_bp.route('/atualizar/<int:id>', methods=['PUT'])
def atualizar_oferta(id):
    oferta = Oferta.query.get(id)
    if not oferta:
        return jsonify({'error': 'Oferta não encontrada.'}), 404

    dados = request.json
    titulo = dados.get('titulo')
    desconto = dados.get('desconto')
    produto_id = dados.get('produto_id')

    if titulo:
        oferta.titulo = titulo
    if desconto is not None:
        oferta.desconto = desconto
    if produto_id:
        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({'error': 'Produto não encontrado.'}), 404
        oferta.produto_id = produto_id

    descricao = dados.get('descricao')
    if descricao is not None:
        oferta.descricao = descricao

    data_inicio_str = dados.get('data_inicio')
    data_fim_str = dados.get('data_fim')
    try:
        if data_inicio_str:
            oferta.data_inicio = datetime.fromisoformat(data_inicio_str)
        if data_fim_str:
            oferta.data_fim = datetime.fromisoformat(data_fim_str)
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use ISO 8601.'}), 400

    Db.session.commit()
    return jsonify(oferta.dados()), 200


# 🔹 Deletar uma oferta
@oferta_bp.route('/excluir/<int:id>', methods=['DELETE'])
def deletar_oferta(id):
    oferta = Oferta.query.get(id)
    if not oferta:
        return jsonify({'error': 'Oferta não encontrada.'}), 404

    # Remover também as associações com produtos
    ProdutoOferta.query.filter_by(oferta_id=id).delete()
    Db.session.delete(oferta)
    Db.session.commit()
    return jsonify({'message': 'Oferta deletada com sucesso.'}), 200


# 🔹 Buscar todos os produtos associados a uma oferta
@oferta_bp.route('/<int:id>/produtos', methods=['GET'])
def listar_produtos_da_oferta(id):
    oferta = Oferta.query.get_or_404(id)
    produtos = [rel.produto.dados() for rel in oferta.produtos_associados]
    return jsonify(produtos), 200


# 🔹 Atualizar produtos de uma oferta
@oferta_bp.route('/<int:id>/produtos', methods=['PUT'])
def atualizar_produtos_da_oferta(id):
    oferta = Oferta.query.get_or_404(id)
    dados = request.json
    novos_ids = dados.get('produtos_ids', [])

    ProdutoOferta.query.filter_by(oferta_id=oferta.id).delete()

    for pid in novos_ids:
        produto = Produto.query.get(pid)
        if produto:
            relacao = ProdutoOferta(produto_id=pid, oferta_id=oferta.id)
            Db.session.add(relacao)

    Db.session.commit()
    return jsonify({"message": "Produtos atualizados com sucesso."}), 200

@oferta_bp.route('/<int:oferta_id>/produtos', methods=['GET'])
def listar_oferta(oferta_id):
    try:
        # Busca os relacionamentos ProdutoOferta com base na oferta_id
        relacoes = ProdutoOferta.query.filter_by(oferta_id=oferta_id).all()

        # Se não houver produtos associados
        if not relacoes:
            return jsonify([]), 200

        # Extrai os produtos relacionados
        produtos = [rel.produto.dados() for rel in relacoes if rel.produto]

        return jsonify(produtos), 200
    except Exception as e:
        print(f"Erro ao buscar produtos da oferta: {e}")
        return jsonify({'erro': 'Erro ao buscar produtos da oferta.'}), 500
    
    