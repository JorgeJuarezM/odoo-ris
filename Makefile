


format:
	find ./addons/ -name "*.py" | xargs python3 -m  autoflake --in-place --remove-all-unused-imports
	find ./addons/ -name "*.py" | xargs python3 -m black 
	find ./addons/ -name "*.py" | xargs python3 -m isort --profile black
	find ./addons/ -name "*.py" | xargs python3 -m flake8
	find ./addons/ -name "*.py" | xargs python3 -m mypy --check-untyped-defs


install:
# 	docker compose run --rm web odoo -d ris -i eden_ris --stop-after-init
	odoo -c /etc/odoo/odoo.conf --db_host db --db_user odoo --db_password odoo -d odoo_ris -i eden_ris --stop-after-init

update:
	docker compose run --rm web odoo -d ris -u eden_ris --stop-after-init
	${MAKE} reload

up:
# 	docker compose up -d
# 	docker compose logs --tail 100 -f web
	odoo -c /etc/odoo/odoo.conf --db_host db --db_user odoo --db_password odoo -d odoo_ris -u eden_ris

reload:
	docker compose stop web
	docker compose up -d