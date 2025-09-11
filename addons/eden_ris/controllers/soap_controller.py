# -*- coding: utf-8 -*-
import io
import logging

from odoo import http
from odoo.api import Environment
from odoo.http import request
from odoo.modules.registry import Registry
from spyne import Application, ServiceBase, Unicode, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.wrappers import Response

_log = logging.getLogger(__name__)

# Namespace (Target Namespace for WSDL)
TNS = "urn:ris.soap.example"


class RisService(ServiceBase):
    @rpc(
        Unicode(pattern="[^\\n\\r]*"),
        _returns=Unicode,
    )
    def SendOrder(ctx, order_id):
        # Access Odoo env injected via WSGI environ (see controller below)
        env = ctx.transport.req["odoo.env"]
        order = env["sale.order"].search([("name", "=", order_id)])
        return str(order.id)


def on_call(ctx):
    env = getattr(ctx.transport, "req", {}).get("odoo.env")
    if env is None:
        # Fallback (should not happen), but keeps service robust
        raise Exception("Odoo env not found")


RisService.event_manager.add_listener("method_call", on_call)


# Spyne Application
soap_application = Application(
    [RisService],
    tns=TNS,
    name="RisSoapService",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)


# WSGI app used by Werkzeug/Odoo bridge
soap_wsgi_app = WsgiApplication(soap_application)


class SoapSpyneController(http.Controller):

    @http.route(
        ["/soap/ris"], auth="public", methods=["GET", "POST"], type="http", csrf=False
    )
    def soap_ris(self, **kwargs):
        """
        Single route handles both WSDL (via `?wsdl`) and SOAP POSTs.
        We delegate the HTTP request to the Spyne WSGI app and return the response.
        """
        if request.httprequest.method == "GET":
            return Response.from_app(soap_wsgi_app, request.httprequest.environ)

        user_id = self.authenticate_basic_auth()
        environ = self.get_wsgi_environ()
        with Registry(request.env.cr.dbname).cursor() as cr:
            environ["odoo.env"] = Environment(cr, user_id, {})
            return Response.from_app(soap_wsgi_app, environ)

    def get_wsgi_environ(self):
        body = request.httprequest.get_data()
        environ = dict(request.httprequest.environ)
        environ["wsgi.input"] = io.BytesIO(body)
        environ["CONTENT_LENGTH"] = str(len(body))
        return environ

    def authenticate_basic_auth(self):
        import base64

        user_credentials = request.httprequest.headers.get("Authorization")
        _, token = user_credentials.split(" ")
        decoded_credentials = base64.b64decode(token)
        username, password = decoded_credentials.split(b":")
        return request.env["res.users"]._login(
            request.env.cr.dbname, username, password, {}
        )
