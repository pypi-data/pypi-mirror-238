import json
from types import NoneType


class Response:
    def __init__(
        self, success: bool = True, msg: str or NoneType = None, data: list = []
    ):
        try:
            assert type(success) == bool, "success is not boolean"
            self.success = success
            assert (
                a := type(msg)
            ) == str or a == NoneType, "msg is not string or None Type"
            self.msg = msg
            assert type(data) == list, "data is not list/array"
            self.data = data
        except Exception as e:
            self.success = False
            self.msg = str(e)
            self.data = []

    def __str__(self):
        return json.dumps({"success": self.success, "msg": self.msg, "data": self.data})

    @property
    def json(self):
        return {
            "success": str(self.success).lower(),
            "msg": self.msg,
            "data": self.data,
        }
