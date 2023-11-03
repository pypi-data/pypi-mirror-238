from typing import Dict, Any
import json_fix # type: ignore
from dataclasses import dataclass
from .locations import Location, get as get_location
from .api import request as api_request
import json
import datetime
from .cache import Cache
from typing import Union, Dict, Optional

api_endpoint = "system.php"

@dataclass
class System:

    system_code: str
    name: str
    start: str
    end: str
    antenna: int
    location_url: str
    location_code: str

    def __json__(self) -> Dict[str, Any]:

        return {
            "system_code": self.system_code,
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "antenna": self.antenna,
            "location_url": self.location_url,
            "location_code": self.location_code
        }

    def location(self) -> Location | None:

        from .locations import get as get_location
        return get_location(self.location_code) 
        

def get(system_code: Optional[str] = None, location: Optional[Union[str, Location]] = None) -> Union[System, Dict[str, System], None]:
    
    if location:

        location_code = location if isinstance(location, str) else location.location_code
        cached_systems = Cache.get("systems")

        if cached_systems:

            all_systems = json.loads(cached_systems).get("data")
            matching_systems = { system_code: system for system_code, system in all_systems.items() if system["location_code"] == location_code }
        
        else:

            payload = {"location_code": location_code}
            response = api_request(api_endpoint, payload)
            matching_systems = response.json()

            if isinstance(matching_systems, dict):

                matching_systems = { matching_systems["system_code"]: matching_systems }

            else:

                matching_systems = { system["system_code"]: system for system in matching_systems }

            for system_code, system in matching_systems.items():

                json_content = {
                    "date": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                    "data": {
                        system_code: system
                    }
                }

                Cache.cache(system_code, json.dumps(json_content, indent=4))

        if len(matching_systems) == 1:

            return System(*next(iter(matching_systems.values())).values())
        
        else:

            return { system_code: System(*system.values()) for system_code, system in matching_systems.items() }  

    elif system_code:

        system = None

        for key in [system_code, "systems"]:

            json_system = Cache.get(key)
            
            if json_system:

                system = json.loads(json_system).get("data").get(system_code)

                if system:

                    break
                
        if not system:

            payload = {
                "system_code": system_code
            }

            response = api_request(api_endpoint, payload)
            json_system =  response.json()

            json_content = {
                "date": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                "data": {
                    system_code: json_system
                }
            }
            
            Cache.cache(system_code, json.dumps(json_content, indent=4))
            system = json_system

        return System(*system.values()) if system else None
    
    else: 

        return None
        

def all() -> Dict[str, System]:

    json_systems = Cache.get("systems")

    if not json_systems:

        response = api_request(api_endpoint)
        json_systems = { system["system_code"] : system for system in response.json() }
    
        json_content = {
            "date": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "data": json_systems
        }

        Cache.cache("systems", json.dumps(json_content, indent=4))

    else:

        json_systems = json.loads(json_systems).get("data")

    systems: dict[str, System] = {}

    for code, json_system in json_systems.items():

        systems[code] = System(*json_system.values())

    return systems