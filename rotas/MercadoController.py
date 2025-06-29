from flask import Blueprint, request, jsonify
import mercadopago

cartao_bp = Blueprint('cartao', __name__, url_prefix='/cartao')

sdk = mercadopago.SDK("TEST-3385419398198282-061917-19421a6e6f2bbaab37ed4b9496115fe7-181091205")

@cartao_bp.route('/pagar', methods=['POST'])
def pagar_cartao():
    data = request.json
    payment_data = {
        "transaction_amount": float(data['valor']),
        "token": data['token'],  # token gerado no frontend
        "description": "Compra no site",
        "installments": int(data.get('parcelas', 1)),
        "payment_method_id": data['metodo_pagamento'],  # exemplo: "visa"
        "payer": {
            "email": data['email'],
            "identification": {
                "type": "CPF",
                "number": data['cpf']
            }
        }
    }

    result = sdk.payment().create(payment_data)
    response = result["response"]

    return jsonify(response)
