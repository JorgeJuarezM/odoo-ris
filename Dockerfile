FROM odoo:17.0

USER root

RUN pip install --upgrade pip && pip install spyne


USER odoo