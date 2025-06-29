import base64
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import SQLAlchemyError
from Model.imagens import Imagem
from conexao import Db

imagem_bp = Blueprint('imagem', __name__, url_prefix='/imagens')


@imagem_bp.route('/Listrar', methods=['GET'])
def listar_imagens():
    imagens = Imagem.query.all()
    return jsonify([img.dados() for img in imagens]), 200

@imagem_bp.route('/disponiveis', methods=['GET'])
def listar_imagens_disponiveis():
    imagens = Imagem.query.filter(Imagem.produto_id == None).all()
    return jsonify([img.dados() for img in imagens]), 200

@imagem_bp.route('/<int:id>', methods=['GET'])
def buscar_imagem(id):
    img = Imagem.query.get_or_404(id)
    return jsonify(img.dados()), 200


@imagem_bp.route('/', methods=['POST'])
def criar_imagem():
    """
    Espera JSON:
    {
        "produto_id": int (opcional),
        "descricao": str (opcional),
        "imagem_base64": str (obrigatório) - base64 da imagem
    }
    """
    data = request.get_json()
    if not data or 'imagem_base64' not in data:
        return jsonify({"error": "Campo 'imagem_base64' é obrigatório."}), 400

    try:
        dados_imagem = base64.b64decode(data['imagem_base64'])
    except Exception:
        return jsonify({"error": "Imagem base64 inválida."}), 400

    novo = Imagem(
        produto_id=data.get('produto_id'),
        descricao=data.get('descricao'),
        dados_imagem=dados_imagem
    )

    try:
        Db.session.add(novo)
        Db.session.commit()
        return jsonify(novo.dados()), 201
    except SQLAlchemyError as e:
        Db.session.rollback()
        return jsonify({"error": "Erro ao salvar a imagem."}), 500


@imagem_bp.route('/<int:id>', methods=['PUT'])
def atualizar_imagem(id):
    """
    Atualiza descrição ou produto_id.
    JSON esperado:
    {
        "produto_id": int (opcional),
        "descricao": str (opcional)
    }
    """
    img = Imagem.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "Nenhum dado enviado."}), 400

    if 'descricao' in data:
        img.descricao = data['descricao']
    if 'produto_id' in data:
        img.produto_id = data['produto_id']

    try:
        Db.session.commit()
        return jsonify(img.dados()), 200
    except SQLAlchemyError:
        Db.session.rollback()
        return jsonify({"error": "Erro ao atualizar a imagem."}), 500


@imagem_bp.route('/<int:id>', methods=['DELETE'])
def deletar_imagem(id):
    img = Imagem.query.get_or_404(id)
    try:
        Db.session.delete(img)
        Db.session.commit()
        return jsonify({"message": f"Imagem {id} deletada com sucesso."}), 200
    except SQLAlchemyError:
        Db.session.rollback()
        return jsonify({"error": "Erro ao deletar a imagem."}), 500
