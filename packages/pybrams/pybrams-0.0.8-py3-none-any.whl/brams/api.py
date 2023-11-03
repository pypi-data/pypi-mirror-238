from typing import Dict, Any
from .http import post

base_url = "https://brams.aeronomie.be/api/v1/"

def request(endpoint: str, payload: Dict[str, Any] | None = None):

    return post(base_url + endpoint, payload)

