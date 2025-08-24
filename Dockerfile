FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    gfortran \
    libblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt

# Define o comando de inicialização
#CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
CMD gunicorn app:app --bind 0.0.0.0:$PORT