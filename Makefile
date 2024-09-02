migrate:
	python manage.py makemigrations
	python manage.py migrate

createuser:
	python manage.py createsuperuser

run:
	python manage.py runserver

static:
	python manage.py collectstatic