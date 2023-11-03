import json
from dataclasses import dataclass
from http.client import OK, UNAUTHORIZED


@dataclass
class HttpResponse:
    status_code: int
    body: [dict, str]
    headers: dict

    def __init__(self, body, *, headers=None):
        self.body = body
        self.headers = headers

    def as_serverless_response(self):
        return {"statusCode": self.status_code,
                "body": json.dumps(self.body, separators=(',', ':')) if isinstance(self.body, dict) else self.body,
                "headers": self.headers}

    def as_server_response(self):
        return self.body, self.status_code


class HttpOk(HttpResponse):
    status_code = int(OK)


class HttpUnauthorized(HttpResponse):
    status_code = int(UNAUTHORIZED)
