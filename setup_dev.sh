#!/bin/sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

attempts=1
max_attempts=30

clear

while [ $attempts -lt $max_attempts ]; do
    if pg_isready -h postgres -p 5432 -U postgres -d postgres; then
        echo "\n${GREEN}================ Banco de dados está pronto, executando migrações... ================${NC}\n"
        python3 manage.py makemigrations
        python3 manage.py migrate

        echo "\n${GREEN}================ Criando superusuário... ================${NC}\n"
        python3 manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true

        # echo "\n${GREEN}================ Iniciando os testes unitários... ================${NC}\n"
        # pytest --no-migrations --disable-warnings -v

        echo "\n${GREEN}================ Iniciando o servidor Django... ================${NC}\n"
        python3 manage.py runserver 0.0.0.0:8000
        break
    else
        echo "\n${YELLOW}Tentativa $attempts: Banco de dados não está pronto. Aguarde um momento, reconectando...${NC}\n"
        attempts=$((attempts+1))
        sleep 5
    fi
done

if [ $attempts -eq $max_attempts ]; then
    echo "${RED}O banco de dados não subiu após $max_attempts tentativas.${NC}"
fi
