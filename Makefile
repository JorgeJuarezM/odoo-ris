ODOO = odoo
ARGS = -c /etc/odoo/odoo.conf --db_host db --db_user odoo \
	--db_password odoo -d odoo_ris --load-language=es_MX --language=es_MX


format:
	find ./addons/ -name "*.py" | xargs python3 -m  autoflake --in-place --remove-all-unused-imports
	find ./addons/ -name "*.py" | xargs python3 -m black 
	find ./addons/ -name "*.py" | xargs python3 -m isort --profile black
	find ./addons/ -name "*.py" | xargs python3 -m flake8
	find ./addons/ -name "*.py" | xargs python3 -m mypy --check-untyped-defs
	find ./addons/ -type f -iname "*.xml" | xargs -I '{}' xmllint --pretty  --format '{}' --output '{}'


install:
# 	docker compose run --rm web odoo -d ris -i eden_ris --stop-after-init
	${ODOO} ${ARGS} -d odoo_ris -i eden_ris --stop-after-init

update:
	${ODOO} ${ARGS} -u eden_ris --stop-after-init
	${MAKE} up

up:
# 	docker compose up -d
# 	docker compose logs --tail 100 -f web
	odoo -c /etc/odoo/odoo.conf --db_host db --db_user odoo --db_password odoo -d odoo_ris -u eden_ris

translate:
	${ODOO} ${ARGS} -d odoo_ris --i18n-export=/mnt/workspace/addons/eden_ris/i18n/es_MX.po --modules=eden_ris --language=es_MX --stop-after-init
