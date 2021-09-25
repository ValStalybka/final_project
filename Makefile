.PHONY: superuser
superuser:
	python3 src/manage.py createsuperuser


.PHONY: migrations
migrations:
	python3 src/manage.py makemigrations


.PHONY: migrate
migrate:
	python3 src/manage.py migrate

.PHONY: collectstatic
collectstatic:
	python3 src/manage.py collectstatic