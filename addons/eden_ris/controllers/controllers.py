# -*- coding: utf-8 -*-
import json
import logging

from jsonpath_ng import parse
from odoo import http

_log = logging.getLogger(__name__)


def get_json_value(json_data, jsonpath_expression):
    try:
        parse_expression = parse(jsonpath_expression)
        values = [match.value for match in parse_expression.find(json_data)]
        return values[0] if values and len(values) == 1 else values
    except Exception:
        _log.exception("Error getting json value")
        return None


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

    @http.route(
        "/api/v1/patient/sync/", auth="none", type="http", csrf=False, methods=["POST"]
    )
    @custom_api_key_auth
    def api_patient_sync(self, **kw):
        """
        {
            "id": 2280804,
            "event_type": "API_PATIENT_UPDATE_ACK",
            "created_at": "2025-09-20T19:12:56.264107+00:00",
            "updated_at": "2025-09-20T19:15:41.147308+00:00",
            "data": {
                "payload": {
                "EVN": {
                    "F0": "EVN",
                    "F1": "",
                    "F2": "20250920131236"
                },
                "MSH": {
                    "F0": "MSH",
                    "F1": "|",
                    "F2": "^~\\&",
                    "F3": "HIS",
                    "F4": {
                    "R1": {
                        "C1": "HESP",
                        "C2": "VER",
                        "C3": "1115"
                    }
                    },
                    "F5": "RIS",
                    "F6": "HESP",
                    "F7": "20250920131241",
                    "F8": "",
                    "F9": {
                    "R1": {
                        "C1": "ADT",
                        "C2": "A01"
                    }
                    },
                    "F10": "0000837462",
                    "F11": "P",
                    "F12": "2.3.1"
                },
                "NK1": {
                    "F0": "NK1",
                    "F1": "1",
                    "F2": {
                    "R1": {
                        "C1": "CAGAL",
                        "C2": "MARIA DEL CARME"
                    }
                    },
                    "F3": "X",
                    "F4": {
                    "R1": {
                        "C1": "C LA MALINCHE 478 A",
                        "C2": "",
                        "C3": "FRACC LOS VOLCANES",
                        "C4": "",
                        "C5": "91770",
                        "C6": "MX"
                    }
                    },
                    "F5": "2293040917"
                },
                "PID": {
                    "F0": "PID",
                    "F1": "",
                    "F2": {
                    "R1": {
                        "C1": "00000000000003064173",
                        "C2": "",
                        "C3": "",
                        "C4": "1"
                    }
                    },
                    "F3": {
                    "R1": {
                        "C1": "1500131807",
                        "C2": "",
                        "C3": "",
                        "C4": "GSM"
                    }
                    },
                    "F4": "",
                    "F5": {
                        "R1": {
                            "C1": "CAGAL",
                            "C2": "MARIA DEL CARMEN",
                            "C3": "ANTELE"
                        }
                    },
                    "F6": "",
                    "F7": "19660826",
                    "F8": "F",
                    "F9": "",
                    "F10": "",
                    "F11": {
                    "R1": {
                        "C1": "C LA MALINCHE 478 A",
                        "C2": "VERACRUZ, VER",
                        "C3": "FRACC LOS VOLCANES",
                        "C4": "VER",
                        "C5": "91770",
                        "C6": "MX"
                    }
                    },
                    "F12": "",
                    "F13": {
                    "R1": {
                        "C1": "2293040917",
                        "C2": "",
                        "C3": "",
                        "C4": "JUAREZELIEL87@GMAIL.COM"
                    }
                    },
                    "F14": "",
                    "F15": "",
                    "F16": "",
                    "F17": "",
                    "F18": "",
                    "F19": "PARTICULAR"
                },
                "PV1": {
                    "F0": "PV1",
                    "F1": "",
                    "F2": "O",
                    "F3": {
                    "R1": {
                        "C1": "VERTRAYX",
                        "C2": "",
                        "C3": ""
                    }
                    },
                    "F4": "",
                    "F5": "",
                    "F6": "",
                    "F7": "",
                    "F8": "",
                    "F9": "",
                    "F10": "",
                    "F11": "",
                    "F12": "",
                    "F13": "",
                    "F14": "",
                    "F15": "",
                    "F16": "",
                    "F17": "",
                    "F18": "",
                    "F19": "1500225315"
                }
                },
                "request": {
                "id": "173361",
                "status": "SUCCESS"
                }
            },
            "external_data": {}
            }
        """
        data = http.request.get_json_data()

        first_name = get_json_value(data, "$.data.payload.PID.F5.R1.C2")
        last_name = " ".join(
            [
                get_json_value(data, "$.data.payload.PID.F5.R1.C1"),
                get_json_value(data, "$.data.payload.PID.F5.R1.C3"),
            ]
        )
        patient_data = {
            "firstname": first_name,
            "lastname": last_name,
            "gender": get_json_value(data, "$.data.payload.PID.F8"),
            "birth_date": get_json_value(data, "$.data.payload.PID.F7"),
        }

        env = http.request.env
        try:
            env["ris.patient"].create(patient_data)
        except Exception as e:
            return http.Response(json.dumps({"error": str(e)}), status=400)
        return http.Response(json.dumps(patient_data), status=200)
