FROM python:3.11-bookworm

WORKDIR /home/app

COPY . .

RUN apt-get update && apt-get install -y \
    postgresql-client tzdata sudo git nano curl gnupg build-essential libpq-dev cron \
    zlib1g-dev libtiff-dev libfreetype6 libfreetype6-dev libwebp-dev libopenjp2-7-dev \
    systemd libreoffice

RUN pip install pipenv --upgrade

RUN pip install setuptools==58.0.4

RUN pipenv install --system --skip-lock

RUN chmod +x setup_dev.sh

ENV PORT 8000
EXPOSE 8000

CMD ["pipenv", "run", "gunicorn", "brain_agriculture.wsgi:application", "--bind", ":8000", "--workers", "1", "--threads", "8"]
