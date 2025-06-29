from flask import Blueprint, jsonify
import requests

cep_bp = Blueprint('cep', __name__, url_prefix='/cep')

@cep_bp.route('/<string:cep>', methods=['GET'])
def consultar_cep(cep):
    try:
        if len(cep) != 8 or not cep.isdigit():
            return jsonify({'erro': 'CEP inválido'}), 400

        response = requests.get(f'https://brasilapi.com.br/api/cep/v1/{cep}')

        if response.status_code != 200:
            print(f'BrasilAPI respondeu {response.status_code}: {response.text}')
            return jsonify({'erro': 'Erro ao consultar BrasilAPI'}), 500

        data = response.json()

        return jsonify({
            'localidade': data.get('city'),
            'uf': data.get('state')
        }), 200

    except Exception as e:
        print(f'Erro no backend ao consultar CEP: {e}')
        return jsonify({'erro': 'Erro interno no servidor'}), 500
