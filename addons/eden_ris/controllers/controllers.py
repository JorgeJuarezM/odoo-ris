# -*- coding: utf-8 -*-
import logging

from odoo import http

_log = logging.getLogger(__name__)


# class EdenRis(http.Controller):
#     @http.route("/eden_ris/eden_ris", auth="public")
#     def index(self, **kw):
#         return "Hello, world 2"

#     @http.route("/eden_ris/eden_ris/objects", auth="public")
#     def list(self, **kw):
#         return http.request.render(
#             "eden_ris.listing",
#             {
#                 "root": "/eden_ris/eden_ris",
#                 "objects": http.request.env["eden_ris.eden_ris"].search([]),
#             },
#         )

#     @http.route(
#         '/eden_ris/eden_ris/objects/<model("eden_ris.eden_ris"):obj>', auth="public"
#     )
#     def object(self, obj, **kw):
#         return http.request.render("eden_ris.object", {"object": obj})

#     @http.route(
#         "/eden_ris/save/", auth="public", methods=["POST"], csrf=False, type="json"
#     )
#     def post(self, **kw):
#         _log.info(http.request)
#         _log.info(dir(http.request))
#         _log.info(http.request.get_json_data())
#         return {"status": "ok"}


def custom_api_key_auth(func):
    def wrapper(*args, **kwargs):
        # api_key = http.request.httprequest.headers.get('X-API-Key')
        # if api_key == 'my_secret_key':
        #     http.request.session.uid = 2
        #     return func(*args, **kwargs)
        # else:
        #     return http.Response("Unauthorized", status=401)
        http.request.session.authenticate("odoo_ris", "admin", "admin")
        return func(*args, **kwargs)

    return wrapper


class EdenRis(http.Controller):
    @http.route(
        "/api/v1/hl7/siu/", auth="none", type="json", csrf=False, methods=["POST"]
    )
    @custom_api_key_auth
    def api_siu(self, **kw):
        env = http.request.env
        data = http.request.get_json_data()
        env["sale.order"].create(
            {
                "name": data["data"]["folio"],
                "partner_id": env.ref("base.res_partner_1").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": data["data"]["description"],
                            "product_id": env.ref("product.product_product_1").id,
                        },
                    )
                ],
            }
        )
        return http.Response("OK", status=400)
