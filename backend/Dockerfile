FROM python:3.9-slim

WORKDIR /app

# Variável de ambiente obrigatória para rodar o Flask pela CLI
ENV FLASK_APP="/app"

# Instala o cliente do PostgreSQL
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copia o script de espera para o contêiner
COPY wait-for-it.sh /wait-for-it.sh

# Copie o script SQL para o contêiner
COPY init_db.sql /app/init_db.sql

# Torna o script executável
RUN chmod +x /wait-for-it.sh

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia o código da aplicação
COPY . .

# Comando para rodar a aplicação Flask após esperar o banco de dados
CMD ["/wait-for-it.sh", "postgres", "--", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]
