from flask import Blueprint, request, jsonify

from Model.imagens import Imagem, Miniatura
from conexao import Db
from PIL import Image
import io
import base64

miniatura_bp = Blueprint('miniatura', __name__, url_prefix='/miniaturas')

# 🔹 Listar todas as miniaturas
@miniatura_bp.route('/listar', methods=['GET'])
def listar_miniaturas():
    miniaturas = Miniatura.query.all()
    return jsonify([{
        "id": m.id,
        "imagem_id": m.imagem_id,
        "miniatura_base64": m.dados_base64()
    } for m in miniaturas]), 200

# 🔹 Buscar miniatura por ID
@miniatura_bp.route('/<int:id>', methods=['GET'])
def obter_miniatura(id):
    miniatura = Miniatura.query.get(id)
    if not miniatura:
        return jsonify({"erro": "Miniatura não encontrada"}), 404

    return jsonify({
        "id": miniatura.id,
        "imagem_id": miniatura.imagem_id,
        "miniatura_base64": miniatura.dados_base64()
    }), 200

# 🔹 Criar miniatura vinculada a uma imagem
@miniatura_bp.route('/criar', methods=['POST'])
def criar_miniatura():
    data = request.json
    imagem_id = data.get('imagem_id')

    imagem = Imagem.query.get(imagem_id)
    if not imagem:
        return jsonify({"erro": "Imagem não encontrada"}), 404

    try:
        # Gera miniatura a partir dos dados da imagem
        img = Image.open(io.BytesIO(imagem.dados_imagem))
        img.thumbnail((100, 100))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        dados_miniatura = buffer.getvalue()

        # Verifica se já existe miniatura
        existente = Miniatura.query.filter_by(imagem_id=imagem_id).first()
        if existente:
            existente.dados_miniatura = dados_miniatura
        else:
            nova = Miniatura(imagem_id=imagem_id, dados_miniatura=dados_miniatura)
            Db.session.add(nova)

        Db.session.commit()
        return jsonify({"sucesso": True, "mensagem": "Miniatura criada ou atualizada com sucesso."}), 201
    except Exception as e:
        Db.session.rollback()
        return jsonify({"erro": str(e)}), 400

# 🔹 Excluir miniatura por ID
@miniatura_bp.route('/excluir/<int:id>', methods=['DELETE'])
def excluir_miniatura(id):
    miniatura = Miniatura.query.get(id)
    if not miniatura:
        return jsonify({"erro": "Miniatura não encontrada"}), 404

    try:
        Db.session.delete(miniatura)
        Db.session.commit()
        return jsonify({"sucesso": True, "mensagem": "Miniatura excluída com sucesso."}), 200
    except Exception as e:
        Db.session.rollback()
        return jsonify({"erro": str(e)}), 400
