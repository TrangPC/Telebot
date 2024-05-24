'''
Tạo class định nghĩa các response cho các API
'''
import json
from flask import Response


class ApiResult:
    server_version = "1.0.0"

    def __init__(self, message: str, res_object: list, errors: list):
        self.message = message
        self.errors = errors
        self.object = res_object
        self.status_code = self.get_http_status_code(message)

    def get_http_status_code(self, message: str) -> int:
        if message == "IDG-00000000":
            status = 200
        elif message == "IDG-00000200":
            status = 200
        elif message == "IDG-00000400":
            status = 400
        elif message == "IDG-00000404":
            status = 404
        elif message == "IDG-00010004":
            status = 408
        else:
            status = 500
        return status

    def get_http_message(self, status_code: int) -> str:
        if status_code == 400:
            http_message = "BAD REQUEST"
        elif status_code == 404:
            http_message = "NOT FOUND"
        elif status_code == 408:
            http_message = "REQUEST TIMEOUT"
        elif status_code == 500:
            http_message = "INTERNAL SERVER ERROR"
        else:
            http_message = "OK"
        return http_message

    def as_dict(self):
        d = {
            "statusCode": self.status_code,
            "message": self.message,
            "server_version": self.server_version,
        }
        if self.errors:
            d["errors"] = self.errors
        if self.object:
            d["object"] = self.object
        return d

    def to_response(self):
        d = self.as_dict()
        response_output = Response(json.dumps(d), status=self.status_code, mimetype="application/json")
        response_output.headers["Access-Control-Allow-Origin"] = "*"
        response_output.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        return response_output

    @classmethod
    def from_errors(cls, message: str, errors: list):
        return cls(message, None, errors)