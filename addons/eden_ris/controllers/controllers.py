# -*- coding: utf-8 -*-
import logging

from odoo import http

_log = logging.getLogger(__name__)


class EdenRis(http.Controller):
    @http.route("/eden_ris/eden_ris", auth="public")
    def index(self, **kw):
        return "Hello, world"

    @http.route("/eden_ris/eden_ris/objects", auth="public")
    def list(self, **kw):
        return http.request.render(
            "eden_ris.listing",
            {
                "root": "/eden_ris/eden_ris",
                "objects": http.request.env["eden_ris.eden_ris"].search([]),
            },
        )

    @http.route(
        '/eden_ris/eden_ris/objects/<model("eden_ris.eden_ris"):obj>', auth="public"
    )
    def object(self, obj, **kw):
        return http.request.render("eden_ris.object", {"object": obj})

    @http.route(
        "/eden_ris/save/", auth="public", methods=["POST"], csrf=False, type="json"
    )
    def post(self, **kw):
        _log.info(http.request)
        _log.info(dir(http.request))
        _log.info(http.request.get_json_data())
        return {"status": "ok"}
