from typing import Dict, Any, Union, Optional
import requests

max_retries = 3
timeout = 10

def get(url: str) -> Optional[requests.Response]:

    retries = 0
    while retries < max_retries:

        try:

            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException:

            retries += 1

    return None

def post(url: str, payload: Optional[Union[Dict[str, Any], None]] = None) -> Optional[requests.Response]:

    retries = 0
    while retries < max_retries:

        try:

            response = requests.post(url, data=payload, timeout=timeout)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException:

            retries += 1

    return None