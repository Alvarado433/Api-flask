from flask import Blueprint, request, jsonify, abort
from datetime import datetime
import base64
from Model.Banner import Banner
from Model.Nivel import Nivel
from Model.Ofertas import Oferta
from conexao import Db

banner_bp = Blueprint('banner', __name__, url_prefix='/banners')

@banner_bp.route('/listar', methods=['GET'])
def listar_banners():
    banners = Banner.query.all()
    resultado = []
    for banner in banners:
        dados_banner = banner.dados()  # seu método atual que retorna os campos básicos
        # Buscar título da oferta associada (se existir)
        if banner.oferta_id:
            oferta = Oferta.query.get(banner.oferta_id)
            if oferta:
                dados_banner['oferta_titulo'] = oferta.titulo
                # Se quiser enviar a oferta inteira:
                # dados_banner['oferta'] = oferta.dados()
        resultado.append(dados_banner)
    return jsonify(resultado), 200

# Buscar banner por ID
@banner_bp.route('/<int:id>', methods=['GET'])
def buscar_banner(id):
    banner = Banner.query.get_or_404(id)
    return jsonify(banner.to_dict()), 200


# Criar um banner
@banner_bp.route('/cadastrar', methods=['POST'])
def cadastrar_banner():
    data = request.json
    titulo = data.get('titulo')
    imagem_base64 = data.get('imagem_base64')  # agora espera base64 da imagem
    oferta_id = data.get('oferta_id')
    nivel_id = data.get('nivel_id')

    if not titulo or not oferta_id:
        return jsonify({"error": "Campos obrigatórios: titulo, oferta_id"}), 400

    # Validar se oferta existe
    oferta = Oferta.query.get(oferta_id)
    if not oferta:
        return jsonify({"error": "Oferta não encontrada"}), 404

    # Validar nível se enviado
    nivel = None
    if nivel_id:
        nivel = Nivel.query.get(nivel_id)
        if not nivel:
            return jsonify({"error": "Nível não encontrado"}), 404

    imagem_blob = None
    if imagem_base64:
        try:
            imagem_blob = base64.b64decode(imagem_base64)
        except Exception:
            return jsonify({"error": "Imagem em base64 inválida"}), 400

    banner = Banner(
        titulo=titulo,
        imagem_blob=imagem_blob,
        oferta_id=oferta_id,
        nivel_id=nivel_id
    )

    Db.session.add(banner)
    Db.session.commit()

    return jsonify(banner.dados()), 201


# Atualizar banner
@banner_bp.route('/<int:id>', methods=['PUT'])
def atualizar_banner(id):
    banner = Banner.query.get_or_404(id)
    data = request.json

    titulo = data.get('titulo')
    imagem_base64 = data.get('imagem_base64')
    oferta_id = data.get('oferta_id')
    nivel_id = data.get('nivel_id')

    if titulo:
        banner.titulo = titulo

    if imagem_base64 is not None:
        if imagem_base64 == "":
            banner.imagem_blob = None
        else:
            try:
                banner.imagem_blob = base64.b64decode(imagem_base64)
            except Exception:
                return jsonify({"error": "Imagem em base64 inválida"}), 400

    if oferta_id:
        oferta = Oferta.query.get(oferta_id)
        if not oferta:
            return jsonify({"error": "Oferta não encontrada"}), 404
        banner.oferta_id = oferta_id

    if nivel_id is not None:
        if nivel_id:
            nivel = Nivel.query.get(nivel_id)
            if not nivel:
                return jsonify({"error": "Nível não encontrado"}), 404
            banner.nivel_id = nivel_id
        else:
            banner.nivel_id = None

    Db.session.commit()
    return jsonify(banner.to_dict()), 200


# Deletar banner
@banner_bp.route('/<int:id>', methods=['DELETE'])
def deletar_banner(id):
    banner = Banner.query.get_or_404(id)
    Db.session.delete(banner)
    Db.session.commit()
    return jsonify({"message": "Banner deletado com sucesso"}), 200
