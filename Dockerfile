# Usa imagem oficial Python slim (leve)
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requirements (ou equivalente) para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código para o container
COPY . .

# Expõe a porta que o app vai rodar (alterar se usar outra)
EXPOSE 8080

# Variável de ambiente para não criar arquivos pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação usando gunicorn
CMD ["gunicorn", "main:servidor", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120"]
