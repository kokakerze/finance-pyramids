ENV = while read LINE; do export $LINE; done < .env
MANAGE = python manage.py
run:
	$(ENV) && $(MANAGE) runserver


new-migrations:
	$(MANAGE)  makemigrations


migrate:
	$(MANAGE)  migrate

lint:
	flake8 .

check:
	$(MANAGE)  check

check-migrations:
	$(MANAGE)  makemigrations --check --dry-run


shell:
	$(MANAGE)  shell_plus --print-sql


createsuperuser:
	$(MANAGE)  createsuperuser


#	python manage.py startapp main
#	mkdir financePyramids1
#	virtualenv venv
#	pip install django
#	mkdir financePyramids1
#	django-admin startproject main
#	django-admin startapp currency

#	pip install Faker
#	pip install django_extensions
#	pip install django-debug-toolbar
#	pip install flower
#	brew install rabbitmq
# 	django -admin startproject

#  celery -A FinancePyramids1 beat -l INFO --scheduler
#