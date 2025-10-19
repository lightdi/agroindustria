FROM python:3.11-slim

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia código do projeto
COPY . .


# Expõe porta
EXPOSE 5001

# Comando para rodar o app (1 worker para evitar problemas com SQLite)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "analises.wsgi:application", "--workers", "1"]
