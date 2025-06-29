from flask import Blueprint, request, jsonify
from Model.CarrinhoItem import CarrinhoItem
from Model.pedido.carrinho import Pedido, PedidoItem
from conexao import Db
from datetime import datetime

pedido_bp = Blueprint('pedido', __name__, url_prefix='/pedido')

@pedido_bp.route('/criar', methods=['POST'])
def criar_pedido():
    try:
        data = request.get_json()
        if not data:
            msg = "JSON inválido ou ausente na requisição"
            print(msg)
            return jsonify({"error": msg}), 400

        usuario_id = data.get('usuario_id')
        if not usuario_id:
            msg = "Usuário não informado"
            print(msg)
            return jsonify({"error": msg}), 400

        # Campos obrigatórios
        campos = {
            "nome_completo": data.get('nome_completo'),
            "cpf": data.get('cpf'),
            "telefone": data.get('telefone'),
            "email": data.get('email'),
            "cep": data.get('cep'),
            "endereco": data.get('endereco'),
            "numero": data.get('numero'),
            "bairro": data.get('bairro'),
            "cidade": data.get('cidade'),
            "estado": data.get('estado'),
        }

        # Verifica quais campos estão faltando ou vazios
        campos_faltando = [k for k, v in campos.items() if not v]
        if campos_faltando:
            msg = f"Campos obrigatórios faltando ou vazios: {', '.join(campos_faltando)}"
            print(msg)
            return jsonify({"error": msg}), 400

        # Buscar itens do carrinho
        carrinho_itens = CarrinhoItem.query.filter_by(usuario_id=usuario_id).all()
        if not carrinho_itens:
            msg = "Carrinho vazio para o usuário"
            print(msg)
            return jsonify({"error": msg}), 400

        # Calcular valor total
        valor_total = 0
        for item in carrinho_itens:
            if not item.produto or not hasattr(item.produto, 'preco'):
                msg = f"Produto inválido no carrinho (ID: {item.produto_id})"
                print(msg)
                return jsonify({"error": msg}), 400
            valor_total += item.produto.preco * item.quantidade

        # Criar pedido
        pedido = Pedido(
            usuario_id=usuario_id,
            nome_completo=campos["nome_completo"],
            cpf=campos["cpf"],
            telefone=campos["telefone"],
            email=campos["email"],
            cep=campos["cep"],
            endereco=campos["endereco"],
            numero=campos["numero"],
            complemento=data.get('complemento', ''),
            bairro=campos["bairro"],
            cidade=campos["cidade"],
            estado=campos["estado"],
            valor_total=valor_total,
            status="pendente",
            data_criacao=datetime.utcnow()
        )

        Db.session.add(pedido)
        Db.session.flush()  # Para ter o pedido.id

        # Criar itens do pedido
        for item in carrinho_itens:
            pedido_item = PedidoItem(
                pedido_id=pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade,
                preco_unitario=item.produto.preco
            )
            Db.session.add(pedido_item)

        # Apagar itens do carrinho
        for item in carrinho_itens:
            Db.session.delete(item)

        Db.session.commit()

        return jsonify({"message": "Pedido criado com sucesso", "pedido_id": pedido.id}), 201

    except Exception as e:
        Db.session.rollback()
        msg = f"Erro ao criar pedido: {str(e)}"
        print(msg)
        return jsonify({"error": msg}), 500

 # Nova rota para listar pedidos de um usuário
@pedido_bp.route('/listar/<int:usuario_id>', methods=['GET'])
def listar_pedidos(usuario_id):
    pedidos = Pedido.query.filter_by(usuario_id=usuario_id).all()

    resultado = []
    for p in pedidos:
        itens = []
        for i in p.itens:
            itens.append({
                "produto_id": i.produto_id,
                "quantidade": i.quantidade,
                "preco_unitario": i.preco_unitario
            })
        resultado.append({
            "id": p.id,
            "nome_completo": p.nome_completo,
            "cpf": p.cpf,
            "telefone": p.telefone,
            "email": p.email,
            "cep": p.cep,
            "endereco": p.endereco,
            "numero": p.numero,
            "complemento": p.complemento,
            "bairro": p.bairro,
            "cidade": p.cidade,
            "estado": p.estado,
            "valor_total": p.valor_total,
            "status": p.status,
            "data_criacao": p.data_criacao.isoformat(),
            "itens": itens
        })

    return jsonify(resultado), 200

@pedido_bp.route('/listar', methods=['GET'])
def listar_pedidos1():
    pedidos = Pedido.query.options(
        Db.joinedload(Pedido.itens).joinedload(PedidoItem.produto)
    ).all()

    result = []
    for pedido in pedidos:
        itens = []
        for item in pedido.itens:
            itens.append({
                "produto_id": item.produto_id,
                "produto_nome": item.produto.nome if item.produto else "Produto não encontrado",
                "quantidade": item.quantidade,
                "preco_unitario": item.preco_unitario,
            })
        
        result.append({
            "id": pedido.id,
            "nome_completo": pedido.nome_completo,
            "cpf": pedido.cpf,
            "telefone": pedido.telefone,
            "valor_total": pedido.valor_total,
            "status": pedido.status,
            "data_criacao": pedido.data_criacao.isoformat(),
            "itens": itens,
        })
    return jsonify(result), 200
