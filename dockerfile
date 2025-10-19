FROM python:3.11

# Diretório de trabalho
WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

# Expõe porta
EXPOSE 5001

# Comando para rodar o app (1 worker para evitar problemas com SQLite)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "analises.wsgi:application", "--workers", "1"]
