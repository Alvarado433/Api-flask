from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import (
    create_access_token, get_jwt_identity,
    jwt_required, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request
)
from Model.Usuario import Usuario

Auth_bp = Blueprint('Autenticar_bp', __name__)

# ROTA DE LOGIN - cria o token e salva em cookie
@Auth_bp.route('/autenticar/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'email' not in data or 'senha' not in data:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400
    
    usuario = Usuario.query.filter_by(email=data['email']).first()
    if not usuario or not usuario.check_senha(data['senha']):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    # ✅ IMPORTANTE: identity deve ser string para evitar erro no JWT
    access_token = create_access_token(identity=str(usuario.id))

    resp = make_response(jsonify({
        "mensagem": f"Bem-vindo, {usuario.nome}!",
        "usuario": usuario.dados()
    }))
    set_access_cookies(resp, access_token)
    return resp


# ROTA DE VERIFICAÇÃO - chamada automática no frontend (AuthContext)
@Auth_bp.route('/verificar', methods=['GET'])
def verificar():
    try:
        # Verifica e extrai identidade do token no cookie
        verify_jwt_in_request()
        user_id = get_jwt_identity()

        # ⚠️ Converter para int, pois o token armazena como string
        usuario = Usuario.query.get(int(user_id))
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        return jsonify({"usuario": usuario.dados()})
    except Exception as e:
        print("ERRO JWT:", e)
        return jsonify({"erro": f"Token inválido: {str(e)}"}), 401


# ROTA DE DASHBOARD PROTEGIDA
@Auth_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    usuario = Usuario.query.get(int(user_id))
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    return jsonify({"mensagem": f"Bem-vindo ao dashboard, {usuario.nome}!"})


# ROTA DE LOGOUT - apaga o cookie JWT
@Auth_bp.route('/autenticar/logout', methods=['POST'])
def logout():
    resp = make_response(jsonify({"mensagem": "Logout efetuado com sucesso"}))
    unset_jwt_cookies(resp)
    return resp
