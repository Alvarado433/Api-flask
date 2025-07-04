from flask import Blueprint, request, jsonify
from Model.CarrinhoItem import CarrinhoItem
from Model.Produto import Produto
from conexao import Db
from flask_jwt_extended import jwt_required, get_jwt_identity

carrinho_bp = Blueprint("carrinho", __name__, url_prefix="/carrinho")

@carrinho_bp.route("/L", methods=["GET"])
@jwt_required(locations=["cookies"])
def listar_carrinho():
    usuario_id = get_jwt_identity()
    print(f"[DEBUG] Listar carrinho - usuario_id: {usuario_id}")
    itens = CarrinhoItem.query.filter_by(usuario_id=usuario_id).all()
    print(f"[DEBUG] Itens no carrinho: {len(itens)}")
    return jsonify([item.dados() for item in itens]), 200

@carrinho_bp.route("/adicionar", methods=["POST"])
@jwt_required(locations=["cookies"])
def adicionar_item():
    usuario_id = get_jwt_identity()
    dados = request.get_json()
    print(f"[DEBUG] Adicionar item - usuario_id: {usuario_id}, dados recebidos: {dados}")

    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade", 1)

    if not produto_id:
        print("[ERROR] produto_id é obrigatório")
        return jsonify({"erro": "produto_id é obrigatório"}), 400

    produto = Produto.query.get(produto_id)
    if not produto:
        print("[ERROR] Produto não encontrado")
        return jsonify({"erro": "Produto não encontrado"}), 404

    item = CarrinhoItem.query.filter_by(usuario_id=usuario_id, produto_id=produto_id).first()
    if item:
        item.quantidade += quantidade
        if item.quantidade > 10:
            item.quantidade = 10
        print(f"[DEBUG] Item existente atualizado - nova quantidade: {item.quantidade}")
    else:
        item = CarrinhoItem(usuario_id=usuario_id, produto_id=produto_id, quantidade=quantidade)
        Db.session.add(item)
        print(f"[DEBUG] Novo item adicionado ao carrinho: produto_id={produto_id}, quantidade={quantidade}")

    Db.session.commit()
    return jsonify(item.dados()), 201

@carrinho_bp.route("/atualizar/<int:item_id>", methods=["PUT"])
@jwt_required(locations=["cookies"])
def atualizar_item(item_id):
    usuario_id = get_jwt_identity()
    dados = request.get_json()
    print(f"[DEBUG] Atualizar item - usuario_id: {usuario_id}, item_id: {item_id}, dados recebidos: {dados}")

    quantidade = dados.get("quantidade")

    if quantidade is None or quantidade < 1 or quantidade > 10:
        print("[ERROR] Quantidade inválida")
        return jsonify({"erro": "Quantidade deve ser entre 1 e 10"}), 400

    item = CarrinhoItem.query.filter_by(id=item_id, usuario_id=usuario_id).first()
    if not item:
        print("[ERROR] Item não encontrado")
        return jsonify({"erro": "Item não encontrado"}), 404

    item.quantidade = quantidade
    Db.session.commit()
    print(f"[DEBUG] Item atualizado - nova quantidade: {quantidade}")
    return jsonify(item.dados()), 200

@carrinho_bp.route("/remover/<int:item_id>", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def remover_item(item_id):
    usuario_id = get_jwt_identity()
    print(f"[DEBUG] Remover item - usuario_id: {usuario_id}, item_id: {item_id}")

    item = CarrinhoItem.query.filter_by(id=item_id, usuario_id=usuario_id).first()
    if not item:
        print("[ERROR] Item não encontrado")
        return jsonify({"erro": "Item não encontrado"}), 404

    Db.session.delete(item)
    Db.session.commit()
    print(f"[DEBUG] Item removido com sucesso")
    return jsonify({"msg": "Item removido"}), 200

@carrinho_bp.route("/limpar", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def limpar_carrinho():
    usuario_id = get_jwt_identity()
    print(f"[DEBUG] Limpar carrinho - usuario_id: {usuario_id}")

    CarrinhoItem.query.filter_by(usuario_id=usuario_id).delete()
    Db.session.commit()
    print(f"[DEBUG] Carrinho limpo com sucesso")
    return jsonify({"msg": "Carrinho limpo"}), 200
