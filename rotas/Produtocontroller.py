import base64
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from Model.Produto import Produto
from Model.imagens import Imagem
from conexao import Db
import unidecode
produto_bp = Blueprint('produto', __name__)

# 🔹 Listar todos os produtos
@produto_bp.route('/produtos/listrar', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([p.dados() for p in produtos]), 200

# 🔹 Buscar produto por ID
@produto_bp.route('/produtos//<int:id>', methods=['GET'])
def produto_por_id(id):
    produto = Produto.query.get_or_404(id)
    return jsonify(produto.dados()), 200

# 🔹 Criar produto
@produto_bp.route('/produtos/cadastrar', methods=['POST'])
def criar_produto():
    data = request.json
    print("DADOS RECEBIDOS:", data)

    try:
        formas_pagamento = data.get('formas_pagamento')
        formas_str = ",".join(formas_pagamento) if isinstance(formas_pagamento, list) else formas_pagamento

        novo_produto = Produto(
            nome=data['nome'],
            preco=data['preco'],
            categoria_id=data['categoria_id'],
            parcelamento=data.get('parcelamento'),
            estoque=data['estoque'],
            pix_valor=data.get('pix_valor'),
            formas_pagamento=formas_str
        )

        Db.session.add(novo_produto)
        Db.session.flush()

        imagens = data.get('imagens', [])
        for img_data in imagens:
            imagem = Imagem(
                produto_id=novo_produto.id,
                imagem_base64=img_data.get('imagem_base64')
            )
            Db.session.add(imagem)

        Db.session.commit()
        return jsonify({"sucesso": True, "produto": novo_produto.dados()}), 201

    except Exception as e:
        Db.session.rollback()
        return jsonify({"sucesso": False, "erro": str(e)}), 400

# 🔹 Atualizar produto existente
@produto_bp.route('/atualizar/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    data = request.json
    try:
        formas_pagamento = data.get('formas_pagamento')
        formas_str = ",".join(formas_pagamento) if isinstance(formas_pagamento, list) else formas_pagamento

        produto.nome = data.get('nome', produto.nome)
        produto.preco = data.get('preco', produto.preco)
        produto.categoria_id = data.get('categoria_id', produto.categoria_id)
        produto.parcelamento = data.get('parcelamento', produto.parcelamento)
        produto.estoque = data.get('estoque', produto.estoque)
        produto.pix_valor = data.get('pix_valor', produto.pix_valor)
        produto.formas_pagamento = formas_str

        Db.session.commit()
        return jsonify({"sucesso": True, "produto": produto.dados()}), 200

    except Exception as e:
        Db.session.rollback()
        return jsonify({"sucesso": False, "erro": str(e)}), 400

# 🔹 Deletar produto
@produto_bp.route('/excluir/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    try:
        Db.session.delete(produto)
        Db.session.commit()
        return jsonify({"sucesso": True, "mensagem": "Produto deletado com sucesso."}), 200
    except Exception as e:
        Db.session.rollback()
        return jsonify({"sucesso": False, "erro": str(e)}), 400

# 🔹 Contar total de produtos
@produto_bp.route('/produtos/contar', methods=['GET'])
def contar_produtos():
    try:
        total = Produto.query.count()
        return jsonify({"total_produtos": total}), 200
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500
@produto_bp.route('/produtos/buscar', methods=['GET'])
def buscar_produtos():
    termo = request.args.get('q', '').strip().lower()
    if not termo:
        return jsonify([]), 200
    
    produtos = Produto.query.filter(Produto.nome.ilike(f'%{termo}%')).all()
    return jsonify([p.dados() for p in produtos]), 200


@produto_bp.route('/produtos/<string:nome>', methods=['GET'])
def buscar_produto_por_nome(nome):
    produto = Produto.query.filter(Produto.nome == nome).first()
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    produto_json = {
        "id": produto.id,
        "nome": produto.nome,
        "preco": produto.preco,
        "estoque": produto.estoque,
        "parcelamento": produto.parcelamento,
        "pix_valor": produto.pix_valor,
        "formas_pagamento": produto.formas_pagamento.split(",") if produto.formas_pagamento else [],
        "categoria": {
            "id": produto.categoria.id,
            "nome": produto.categoria.nome,
        } if produto.categoria else None,
        # Aqui chama o método dados() da Imagem para pegar o base64 corretamente
        "imagens": [img.dados() for img in produto.imagens] if produto.imagens else [],
        "ofertas": [rel.oferta.dados() for rel in produto.ofertas_associadas] if produto.ofertas_associadas else []
    }

    return jsonify(produto_json)
@produto_bp.route('/produtos/nome/<string:slug>', methods=['GET'])
def buscar_por_nome(slug):
    nome_param = slug.replace('-', ' ')
    nome_param = unidecode.unidecode(nome_param).lower()

    produtos = Produto.query.all()

    produto = next((p for p in produtos if unidecode.unidecode(p.nome).lower() == nome_param), None)

    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    imagens = [
        {'imagem_base64': base64.b64encode(img.dados_imagem).decode('utf-8') if img.dados_imagem else None}
        for img in produto.imagens
    ]

    return jsonify({
        'id': produto.id,
        'nome': produto.nome,
        'preco': produto.preco,
        'estoque': produto.estoque,
        'parcelamento': produto.parcelamento,
        'pix_valor': produto.pix_valor,
        'formas_pagamento': produto.formas_pagamento.split(",") if produto.formas_pagamento else [],
        'imagens': imagens
    })

@produto_bp.route('/produtos/desvincular-categoria/<int:categoria_id>', methods=['PUT'])
def desvincular_categoria(categoria_id):
    produtos = Produto.query.filter_by(categoria_id=categoria_id).all()
    for p in produtos:
        p.categoria_id = None
    Db.session.commit()
    return jsonify({"message": "Produtos desvinculados com sucesso"}), 200
