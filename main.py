import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from conexao import Db
from conexao.conexao import Configuracao
from conexao.email import mail

# Importação dos blueprints (exemplo)
from rotas.usuarioController import usuario_bp
from rotas.nivelController import nivel_bp
from rotas.Produtocontroller import produto_bp
from rotas.imagemController import imagem_bp
from rotas.CategoriaController import categoria_bp
from rotas.OfertasControllers import oferta_bp
from rotas.BannerController import banner_bp
from rotas.MercadoController import cartao_bp
from rotas.pix import pix_bp
from rotas.AuthController import Auth_bp
from rotas.miniatura_controller import miniatura_bp
from rotas.CupomController import cupom_bp
from rotas.carrinho_controller import carrinho_bp
from rotas.pedidocontroller import pedido_bp
from rotas.cepcontroller import cep_bp
from rotas.EmailController import email_bp

# Inicialização da aplicação Flask
servidor = Flask(__name__)

# Configurações gerais do app
servidor.config.from_object(Configuracao)

# Configuração do JWT
servidor.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Nunca deixar hardcoded

# Configuração para desenvolvimento vs produção
if os.getenv("FLASK_ENV") == "development":
    servidor.config["JWT_COOKIE_SECURE"] = False  # HTTP no localhost
    servidor.config["JWT_COOKIE_SAMESITE"] = "Lax"  # Funciona para localhost
else:
    servidor.config["JWT_COOKIE_SECURE"] = True   # HTTPS em produção
    servidor.config["JWT_COOKIE_SAMESITE"] = "None"  # Cross-site cookie permitido

# DESATIVA CSRF para facilitar teste (habilitar somente se implementar token CSRF no frontend)
servidor.config["JWT_COOKIE_CSRF_PROTECT"] = False

# Localização dos tokens JWT no cookie
servidor.config["JWT_TOKEN_LOCATION"] = ["cookies"]
servidor.config["JWT_ACCESS_COOKIE_PATH"] = "/"

jwt = JWTManager(servidor)

# Configuração do CORS - permitir frontend específico e enviar cookies
CORS(
    servidor,
    supports_credentials=True,
    resources={r"/*": {"origins": ["https://imperio-store.vercel.app", "http://localhost:3000"]}},
)

# Configurações do e-mail (Gmail)
servidor.config['MAIL_SERVER'] = 'smtp.gmail.com'
servidor.config['MAIL_PORT'] = 587
servidor.config['MAIL_USE_TLS'] = True
servidor.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
servidor.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail.init_app(servidor)

# Inicializar DB e Migrate
Db.init_app(servidor)
migrate = Migrate(servidor, Db)

# Registrar blueprints
servidor.register_blueprint(usuario_bp)
servidor.register_blueprint(nivel_bp)
servidor.register_blueprint(produto_bp)
servidor.register_blueprint(imagem_bp)
servidor.register_blueprint(categoria_bp)
servidor.register_blueprint(oferta_bp)
servidor.register_blueprint(banner_bp)
servidor.register_blueprint(cartao_bp)
servidor.register_blueprint(pix_bp)
servidor.register_blueprint(Auth_bp)
servidor.register_blueprint(miniatura_bp)
servidor.register_blueprint(cupom_bp)
servidor.register_blueprint(carrinho_bp)
servidor.register_blueprint(pedido_bp)
servidor.register_blueprint(cep_bp)
servidor.register_blueprint(email_bp)

# Rota simples de teste
@servidor.route('/')
def home():
    return jsonify({"mensagem": "Bem-vindo à API"})

# Rodar a aplicação
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.getenv("FLASK_ENV") == "development"
    servidor.run(host="0.0.0.0", port=port, debug=debug_mode)
