from flask import Blueprint, jsonify, request
import mercadopago

pix_bp = Blueprint('pix', __name__, url_prefix='/pix')

# Token de testes Mercado Pago (sandbox)
sdk = mercadopago.SDK("TEST-3385419398198282-061917-19421a6e6f2bbaab37ed4b9496115fe7-181091205")

@pix_bp.route('/criar', methods=['POST'])
def gerar_pix():
    data = request.get_json()

    try:
        # Verifica se os campos obrigatórios existem
        valor = data.get("valor")
        email = data.get("email")
        nome = data.get("nome", "Cliente")

        if not valor or not email:
            return jsonify({"error": "Parâmetros 'valor' e 'email' são obrigatórios."}), 400

        # Monta o payload para pagamento Pix
        payment_data = {
            "transaction_amount": float(valor),
            "payment_method_id": "pix",
            "description": f"Pagamento Pix - Pedido para {nome}",
            "payer": {
                "email": email,
                "first_name": nome,
            }
        }

        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]

        # Verifica se retornou dados de QR Code
        if payment.get("status") in ["pending", "approved"]:
            transaction_data = payment.get("point_of_interaction", {}).get("transaction_data", {})
            qr_code_base64 = transaction_data.get("qr_code_base64")
            qr_code = transaction_data.get("qr_code")

            if qr_code_base64 and qr_code:
                return jsonify({
                    "qr_code_base64": qr_code_base64,
                    "qr_code": qr_code,
                    "status": payment["status"]
                }), 201
            else:
                return jsonify({"error": "QR Code não disponível na resposta"}), 500

        return jsonify({"error": "Falha ao gerar pagamento"}), 400

    except Exception as e:
        print("Erro ao gerar pagamento Pix:", e)
        return jsonify({"error": "Erro interno"}), 500
