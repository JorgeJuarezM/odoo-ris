FROM mcr.microsoft.com/devcontainers/base:jammy




# Install Odoo
ENV ODOO_VERSION=17.0
ARG ODOO_RELEASE=20250819
ARG ODOO_SHA=f342ea8c4ac7944ecee4b7f023903fd528f988e6
RUN curl -o odoo.deb -sSL http://nightly.odoo.com/${ODOO_VERSION}/nightly/deb/odoo_${ODOO_VERSION}.${ODOO_RELEASE}_all.deb \
    && echo "${ODOO_SHA} odoo.deb" | sha1sum -c - \
    && apt-get update \
    && apt-get -y install --no-install-recommends ./odoo.deb \
    && apt-get -y install python3-pip \
    && rm -rf /var/lib/apt/lists/* odoo.deb


RUN mkdir -p /var/lib/odoo
RUN groupadd odooadm

RUN usermod -aG odooadm odoo
RUN usermod -aG odooadm vscode
# RUN chgrp -R odooadm /var/lib/odoo
RUN chown -R odoo:odooadm /var/lib/odoo
RUN chmod -R 770 /var/lib/odoo



COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Set permissions and Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN chown odoo /etc/odoo/odoo.conf \
&& mkdir -p /mnt/extra-addons \
&& chown -R odoo /mnt/extra-addons

VOLUME ["/var/lib/odoo", "/mnt/extra-addons", "/mnt/workspace"]





# RUN usermod -s /bin/bash odoo

USER odoo