from typing import Optional

import os
import uuid
import json
import requests
import datetime


class Trace:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name

class Safelayer:
    _apiKey = os.environ.get("SAFELAYER_API_KEY")
    _apiUrl = os.environ.get("SAFELAYER_API_URL") or "https://api.repllabs.com/v1"

    @classmethod
    def init(cls, apiKey: Optional[str] = None):
        if apiKey:
            cls._apiKey = apiKey

        if not cls._apiKey:
            raise ValueError("API key is missing.")

    @classmethod
    def log(
        cls,
        trace: Trace,
        trace_done=True,
        data={},
        metadata={},
    ):
        trace_data = {**trace.__dict__, "done": trace_done} 

        payload = {
            "time": datetime.datetime.utcnow().isoformat(),
            "trace": trace_data,
            "data": data,
            "metadata": metadata,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cls._apiKey}",
        }

        response = requests.post(
            f"{cls._apiUrl}/log", headers=headers, data=json.dumps(payload)
        )

        return response


trace = lambda name: Trace(name)
init = Safelayer.init
log = Safelayer.log
