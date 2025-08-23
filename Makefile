


format:
	find ./addons/ -name "*.py" | xargs python -m black 
	find ./addons/ -name "*.py" | xargs python -m isort --profile black
	find ./addons/ -name "*.py" | xargs python -m flake8
	find ./addons/ -name "*.py" | xargs python -m mypy --check-untyped-defs

install:
	docker compose run --rm web odoo -d ris -i eden_ris --stop-after-init

update:
	docker compose run --rm web odoo -d ris -u eden_ris --stop-after-init
	${MAKE} reload

up:
	docker compose up -d
	docker compose logs --tail 100 -f web

reload:
	docker compose stop web
	docker compose up -d