
# Docker containers
up:
	docker-compose up --build -d

down:
	docker-compose down

restart:
	docker-compose restart

# Application commands
runserver:
	docker-compose exec web uv run python manage.py runserver 0.0.0.0:8000

migrations:
	docker-compose exec web uv run python manage.py makemigrations

migrate:
	docker-compose exec web uv run python manage.py migrate

shell:
	docker-compose exec web uv run python manage.py shell

test:
	docker-compose exec web uv run python manage.py test

superuser:
	docker-compose exec web uv run python manage.py createsuperuser

# Scripts
populate:
	docker-compose exec web uv run python manage.py runscript populate_db

query:
	docker-compose exec web uv run python manage.py runscript query

# Cleanup
clean:
	python -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyo')]"



clean-docker:
	docker-compose down -v --remove-orphans
	docker system prune -f