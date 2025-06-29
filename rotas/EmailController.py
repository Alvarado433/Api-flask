from flask import Blueprint, request, jsonify
from flask_mail import Message
from conexao.email import mail # Certifique-se que o "mail" está sendo importado do seu app principal

email_bp = Blueprint('email', __name__, url_prefix='/email')


@email_bp.route('/enviar', methods=['POST'])
def enviar_email():
    try:
        data = request.get_json()

        destinatario = data.get('destinatario')
        assunto = data.get('assunto', 'Mensagem da Loja')
        mensagem = data.get('mensagem')

        if not destinatario or not mensagem:
            return jsonify({"error": "Destinatário e mensagem são obrigatórios"}), 400

        msg = Message(assunto,
                      sender=('Loja Online', 'seuemail@gmail.com'),
                      recipients=[destinatario])
        msg.body = mensagem

        mail.send(msg)

        return jsonify({"message": "E-mail enviado com sucesso"}), 200

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return jsonify({"error": "Erro ao enviar e-mail"}), 500
