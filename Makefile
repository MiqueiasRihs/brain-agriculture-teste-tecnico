run:
	python manage.py runserver 0.0.0.0:8000
migrate:
	python manage.py makemigrations
	python manage.py migrate
static:
	echo "yes" | python manage.py collectstatic
shell:
	python manage.py shell
test:
	pytest --no-migrations --disable-warnings -v
