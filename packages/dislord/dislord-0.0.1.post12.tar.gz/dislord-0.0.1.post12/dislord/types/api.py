from dataclasses import dataclass
from http.client import OK, UNAUTHORIZED


@dataclass
class HttpResponse:
    status_code: int
    body: dict
    headers: dict

    def __init__(self, body, *, headers=None):
        self.body = body
        self.headers = headers

    def as_serverless_response(self):
        return {"statusCode": self.status_code,
                "body": self.body,
                "headers": self.headers}

    def as_server_response(self):
        return self.body, self.status_code


class HttpOk(HttpResponse):
    status_code = OK


class HttpUnauthorized(HttpResponse):
    status_code = UNAUTHORIZED
