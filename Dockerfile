FROM python:3.11-bookworm

# Diretório de trabalho
WORKDIR /home/app

# Copia todos os arquivos para o diretório de trabalho
COPY . .

# Instala as dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client tzdata sudo git nano curl gnupg build-essential libpq-dev cron \
    zlib1g-dev libtiff-dev libfreetype6 libfreetype6-dev libwebp-dev libopenjp2-7-dev \
    systemd libreoffice

# Instala o Pipenv
RUN pip install pipenv --upgrade

# Instala uma versão específica do setuptools
RUN pip install setuptools==58.0.4

# Cria e ativa o ambiente virtual antes de instalar as dependências
RUN pipenv install --system --skip-lock

# Garante que o script setup_dev.sh seja executável
RUN chmod +x setup_dev.sh

# Define a variável de ambiente para a porta e expõe a porta
ENV PORT 8000
EXPOSE 8000

# Comando para iniciar o aplicativo
CMD ["pipenv", "run", "gunicorn", "brain_agriculture.wsgi:application", "--bind", ":8000", "--workers", "1", "--threads", "8"]
