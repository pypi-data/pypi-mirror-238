from datetime import datetime
from typing import Tuple, Union

def parse(interval_str: str) -> Union[Tuple[datetime, Union[datetime, None]], None]:

    try:

        if "/" in interval_str:

            start_str, end_str = interval_str.split("/")

        else:

            start_str = interval_str
            end_str = None

        start_datetime = datetime.fromisoformat(start_str)
        end_datetime = datetime.fromisoformat(end_str) if end_str else None

        return start_datetime, end_datetime

    except ValueError:

        return None