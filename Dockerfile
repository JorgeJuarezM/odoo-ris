FROM odoo:17.0

USER root

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER odoo
ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]