FROM odoo:17.0

USER root

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt


USER odoo