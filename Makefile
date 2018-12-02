clean:
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete
	find . -type f -name "*.pid" -delete
	find . -type f -name "*.sqlite" -delete
	find . -type f -name "*_cookie_*" -delete
	find . -type f -name "*coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

pip:
	./venv/bin/pip install -r requirements.txt

migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

install:
	pip install -r requirements.txt

run:
	python manage.py runserver

importanize:
	find src -type f -name "*.py" | xargs ./env/bin/importanize
	find tests -type f -name "*.py" | xargs ./env/bin/importanize
test:
	python manage.py test

docker:
	docker build -t "docker.hub.com/{username}/django_app:1.0.0" .
	docker push docker.hub.com/{username}/django_app:1.0.0
