from flask import Blueprint, request, jsonify
from datetime import datetime, time, timedelta, timezone
from Model.Cupom import Cupom
from Model.Nivel import Nivel
from conexao import Db

cupom_bp = Blueprint("cupom", __name__)

def str_to_datetime_end_of_day(date_str: str):
    """
    Converte string 'YYYY-MM-DD' para datetime no final do dia (23:59:59) UTC.
    """
    date_only = datetime.strptime(date_str, "%Y-%m-%d")
    # Ajusta para UTC e fim do dia
    dt_utc = datetime.combine(date_only.date(), time(23, 59, 59, tzinfo=timezone.utc))
    return dt_utc


# Listar todos os cupons
@cupom_bp.route("/cupons/listar", methods=["GET"])
def listar_cupons():
    cupons = Cupom.query.all()
    return jsonify([c.Dados() for c in cupons]), 200


# Criar cupom genérico
@cupom_bp.route("/cupons/cadastrar", methods=["POST"])
def criar_cupom():
    data = request.json

    if not data.get("codigo") or not data.get("statusId"):
        return jsonify({"erro": "Campos obrigatórios: codigo, statusId"}), 400

    status = Nivel.query.get(data["statusId"])
    if not status:
        return jsonify({"erro": "statusId inválido"}), 400

    validade = None
    if data.get("validade"):
        validade = str_to_datetime_end_of_day(data["validade"])

    if data.get("freeShipping", False):
        min_price = 0.0
        max_price = None
        desconto = None
        descricao = None
    else:
        if not data.get("minPrice"):
            return jsonify({"erro": "minPrice é obrigatório para cupons que não são frete grátis"}), 400
        min_price = data["minPrice"]
        max_price = data.get("maxPrice")
        desconto = data.get("discount")
        descricao = data.get("label")

    novo = Cupom(
        codigo=data["codigo"].upper(),
        min_price=min_price,
        max_price=max_price,
        desconto=desconto,
        frete_gratis=data.get("freeShipping", False),
        descricao=descricao,
        status_id=data["statusId"],
        validade=validade
    )

    Db.session.add(novo)
    Db.session.commit()

    return jsonify(novo.Dados()), 201


# Editar cupom
@cupom_bp.route("/cupons/<string:codigo>", methods=["PUT"])
def editar_cupom(codigo):
    cupom = Cupom.query.filter_by(codigo=codigo.upper()).first()
    if not cupom:
        return jsonify({"erro": "Cupom não encontrado"}), 404

    data = request.json

    if "statusId" in data:
        status = Nivel.query.get(data["statusId"])
        if not status:
            return jsonify({"erro": "statusId inválido"}), 400
        cupom.status_id = data["statusId"]

    if "minPrice" in data:
        cupom.min_price = data["minPrice"]

    if "maxPrice" in data:
        cupom.max_price = data["maxPrice"]

    if "discount" in data:
        cupom.desconto = data["discount"]

    if "freeShipping" in data:
        cupom.frete_gratis = data["freeShipping"]

    if "label" in data:
        cupom.descricao = data["label"]

    if "validade" in data:
        if data["validade"]:
            cupom.validade = str_to_datetime_end_of_day(data["validade"])
        else:
            cupom.validade = None

    Db.session.commit()
    return jsonify(cupom.Dados()), 200


# Trocar status do cupom (PATCH)
@cupom_bp.route("/cupons/<string:codigo>/status", methods=["PATCH"])
def trocar_status(codigo):
    cupom = Cupom.query.filter_by(codigo=codigo.upper()).first()
    if not cupom:
        return jsonify({"erro": "Cupom não encontrado"}), 404

    data = request.json
    novo_status_id = data.get("statusId")

    if novo_status_id is None:
        return jsonify({"erro": "statusId é obrigatório"}), 400

    status = Nivel.query.get(novo_status_id)
    if not status:
        return jsonify({"erro": "statusId inválido"}), 400

    cupom.status_id = novo_status_id
    Db.session.commit()

    return jsonify({"codigo": cupom.codigo, "novoStatusId": cupom.status_id}), 200


# Excluir cupom
@cupom_bp.route("/cupons/<string:codigo>", methods=["DELETE"])
def excluir_cupom(codigo):
    cupom = Cupom.query.filter_by(codigo=codigo.upper()).first()
    if not cupom:
        return jsonify({"erro": "Cupom não encontrado"}), 404

    Db.session.delete(cupom)
    Db.session.commit()

    return jsonify({"mensagem": f"Cupom '{codigo}' excluído com sucesso."}), 200


# Contar cupons
@cupom_bp.route("/cupons/count", methods=["GET"])
def contar_cupons():
    total = Db.session.query(Cupom).count()
    return jsonify({'count': total}), 200


# Criar cupom frete grátis genérico (com validade enviada)
@cupom_bp.route("/cupons/frete-gratis", methods=["POST"])
def criar_cupom_frete_gratis():
    data = request.json
    codigo = data.get("codigo")
    validade_str = data.get("validade")

    if not codigo or not validade_str:
        return jsonify({"erro": "Campos obrigatórios: codigo, validade"}), 400

    try:
        # Tenta aceitar ISO com ou sem milissegundos e com 'Z'
        validade = None
        formatos = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]
        for fmt in formatos:
            try:
                validade = datetime.strptime(validade_str, fmt)
                break
            except ValueError:
                continue
        if validade is None:
            return jsonify({"erro": "Formato de data inválido"}), 400

        validade = validade.replace(tzinfo=timezone.utc)
        # Define fim do dia UTC
        validade = datetime.combine(validade.date(), time(23, 59, 59, tzinfo=timezone.utc))
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar validade: {str(e)}"}), 400

    cupom_existente = Cupom.query.filter_by(codigo=codigo.upper()).first()
    if cupom_existente:
        return jsonify({"erro": "Cupom já existe"}), 409

    status_ativo = Nivel.query.filter_by(nome="Ativo").first()
    if not status_ativo:
        return jsonify({"erro": "Nível 'Ativo' não encontrado"}), 400

    novo_cupom = Cupom(
        codigo=codigo.upper(),
        min_price=0,
        max_price=None,
        desconto=0,
        frete_gratis=True,
        descricao="Cupom automático de frete grátis",
        status_id=status_ativo.id,
        validade=validade
    )
    Db.session.add(novo_cupom)
    Db.session.commit()

    return jsonify({"mensagem": "Cupom de frete grátis criado", "codigo": novo_cupom.codigo}), 201


# Criar cupom frete grátis válido por 24 horas a partir do momento da criação (usando UTC)
@cupom_bp.route("/cupons/frete-gratis-24h", methods=["POST"])
def criar_cupom_frete_gratis_24h():
    data = request.json
    codigo = data.get("codigo")

    if not codigo:
        return jsonify({"erro": "Campo obrigatório: codigo"}), 400

    cupom_existente = Cupom.query.filter_by(codigo=codigo.upper()).first()
    if cupom_existente:
        return jsonify({"erro": "Cupom já existe"}), 409

    status_ativo = Nivel.query.filter_by(nome="Ativo").first()
    if not status_ativo:
        return jsonify({"erro": "Nível 'Ativo' não encontrado"}), 400

    validade = datetime.now(timezone.utc) + timedelta(hours=24)

    novo_cupom = Cupom(
        codigo=codigo.upper(),
        min_price=0,
        max_price=None,
        desconto=0,
        frete_gratis=True,
        descricao="Cupom automático de frete grátis por 24h",
        status_id=status_ativo.id,
        validade=validade
    )
    Db.session.add(novo_cupom)
    Db.session.commit()

    return jsonify({
        "mensagem": "Cupom de frete grátis criado com validade de 24h",
        "codigo": novo_cupom.codigo,
        "validade": novo_cupom.validade.isoformat()
    }), 201


@cupom_bp.route("/cupons/frete-gratis-24h/ativo", methods=["GET"])
def buscar_cupom_frete_gratis_ativo():
    agora = datetime.now(timezone.utc)

    cupom = (
        Cupom.query
        .filter(
            Cupom.frete_gratis == True,
            Cupom.validade >= agora,
            Cupom.nivel.has(nome="Ativo")   # <-- Aqui corrigido para 'nivel'
        )
        .order_by(Cupom.validade.desc())
        .first()
    )
    if not cupom:
        return jsonify({"erro": "Nenhum cupom de frete grátis válido encontrado"}), 404

    return jsonify({
        "codigo": cupom.codigo,
        "validade": cupom.validade.isoformat(),
        "descricao": cupom.descricao
    }), 200
