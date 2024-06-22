FROM python:3.9-slim

WORKDIR /app

# variável de ambiente obrigatória para rodar o Flask pela CLI
ENV FLASK_APP="/app"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
# CMD ["python", "app.py"]
