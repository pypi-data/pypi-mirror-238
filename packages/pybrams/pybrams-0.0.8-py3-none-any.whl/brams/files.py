from __future__ import annotations
from types import NoneType
from typing import Any, Dict, Literal, Optional, Union, List
import json_fix # type: ignore
import os
import json
from . import locations
from . import systems
from .wav import Wav
from .signal import Signal
from .pps import PPS
from .api import request as api_request
from .http import get as get_request
from .cache import Cache
from .interval import parse

api_endpoint = "file.php"

class File:

    def __init__(self, year: int, month: int, day: int, hours: int, minutes: int, samplerate: float,
                 pps_count: int, duration: int, precise_start: int, precise_end: int, system_code: str,
                 location_code: str, location_url: str, system_url: str, wav_url: str, wav_name: str, png_url: str,
                 png_name: str, beacon_frequency: Optional[float] = None):

        self.year: int = year
        self.month: int = month
        self.day: int = day
        self.hours: int = hours
        self.minutes: int = minutes
        self.samplerate: float = samplerate
        self.pps_count: int = pps_count
        self.duration: int = duration
        self.precise_start: int = precise_start
        self.precise_end: int = precise_end
        self.system_code: str = system_code
        self.location_code: str = location_code
        self.location_url: str = location_url
        self.system_url: str = system_url
        self.wav_url: str = wav_url
        self.wav_name: str = wav_name
        self.png_url: str = png_url
        self.png_name: str = png_name
        self.beacon_frequency: Optional[float] = beacon_frequency

        self.signal: Optional[Signal] = None

        self.corrected_wav_name = f"{self.wav_name[:-4]}.corrected.wav" if self.wav_name else None
        self.type = "AR" if "BEHUMA" in self.system_code else "RSP2" if self.samplerate == 6048 else "ICOM"
        self.wav: Optional[Wav] = None

    def __json__(self) -> Dict[str, Any]:

        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hours": self.hours,
            "minutes": self.minutes,
            "sample_rate": self.samplerate,
            "pps_count": self.pps_count,
            "duration": self.duration,
            "precise_start": self.precise_start,
            "precise_end": self.precise_end,
            "system_code": self.system_code,
            "location_code": self.location_code,
            "location_url": self.location_url,
            "system_url": self.system_url,
            "wav_url": self.wav_url,
            "wav_name": self.wav_name,
            "png_url": self.png_url,
            "png_name": self.png_name,
            "beacon_frequency": self.signal.beacon_frequency if self.signal else None
        }
    
    def system(self) -> systems.System | None:

        return systems.get(self.system_code) 


    def location(self) -> locations.Location | None:

        return locations.get(self.location_code) 


    def load(self) -> None:

        wav_content = Cache.get(self.wav_name, False)

        if not wav_content:

            while not wav_content or not len(wav_content):

                response = get_request(self.wav_url)
                wav_content = response.content

            Cache.cache(self.wav_name, wav_content, False)

        self.wav = Wav(wav_content)
        self.pps = PPS(self.wav.pps.index, self.wav.pps.time)
        self.signal = Signal(self.wav.header.samplerate, self.wav.data.signal, self.beacon_frequency)


    def save(self, path: str = ".") -> None:

        self.load() if not self.wav else None

        if self.wav:

            with open(os.path.join(path, self.wav_name), "wb") as file:

                file.write(self.wav.write())


    def process(self) -> None:

        corrected_wav_content = Cache.get(self.corrected_wav_name, False)

        if not corrected_wav_content:

            self.load() if not self.wav else None

            self.corrected_pps = self.pps.to_corrected_PPS(self.type)
            self.wav.pps.pps = [val for pair in zip(self.corrected_pps.index, self.corrected_pps.time) for val in pair]

            self.signal = Signal(self.wav.header.samplerate, self.wav.data.signal)
            self.signal.process()
            self.beacon_frequency = self.signal.beacon_frequency
            self.wav.data.set(self.signal)

            Cache.cache(self.json_string(), json.dumps(self, indent=4))
            Cache.cache(self.corrected_wav_name, self.wav.write(), False)

        else:

            self.wav = Wav(corrected_wav_content)
            self.pps = PPS(self.wav.pps.index, self.wav.pps.time)
            self.signal = Signal(self.wav.header.samplerate, self.wav.data.signal, self.beacon_frequency)
            self.signal.compute_fft()


    def json_string(self) -> str:

        return f"{self.system_code}.{str(self.year).zfill(4)}{str(self.month).zfill(2)}{str(self.day).zfill(2)}_{str(self.hours).zfill(2)}{str(self.minutes).zfill(2)}"


    def __add__(self, other: File) -> File | None:

        # WIP

        if self.system_code == other.system_code and self.type == other.type:

            import numpy as np

            samplerate = np.mean([self.samplerate, other.samplerate])
            pps_count = self.pps_count + other.pps_count
            duration = self.duration + other.duration

            return File(self.year, self.month, self.day, self.hours, self.minutes, samplerate, pps_count, duration, self.precise_start, other.precise_end, self.system_code, self.location_code, self.location_url, self.system_url, None, None, None, None)

        return None


    def __eq__(self, other: File) -> bool:

        if isinstance(other, File):

            return (
                self.year == other.year and
                self.month == other.month and
                self.day == other.day and
                self.hours == other.hours and
                self.minutes == other.minutes and
                self.samplerate == other.samplerate and
                self.pps_count == other.pps_count and
                self.duration == other.duration and
                self.precise_start == other.precise_start and
                self.precise_end == other.precise_end and
                self.system_code == other.system_code and
                self.location_code == other.location_code and
                self.location_url == other.location_url and
                self.system_url == other.system_url and
                self.wav_url == other.wav_url and
                self.wav_name == other.wav_name and
                self.png_url == other.png_url and
                self.png_name == other.png_name and
                self.corrected_wav_name == other.corrected_wav_name and
                self.type == other.type and
                self.signal == other.signal
            )

        return False


def get(interval: str, system: Union[str, systems.System, List[Union[str, systems.System]], Dict[str, systems.System], None] = None) -> Union[File, Dict[str, File], Dict[str, List[File]] | None]:

    def get_file(system_code, key: str):

        cached_file = Cache.get(key)
        
        if cached_file:

            return File(*json.loads(cached_file).values())

        payload = {
            "start": start,
            "system_code": system_code
        }
        
        response = api_request(api_endpoint, payload)
        json_file = response.json()

        if json_file:

            file = File(*json_file.values())
            Cache.cache(key, json.dumps(file, indent=4))
            return file
    
        return None

    def process(start, system):  

        if isinstance(system, str):

            key = f"{system}.{str(start.year).zfill(4)}{str(start.month).zfill(2)}{str(start.day).zfill(2)}_{str(start.hour).zfill(2)}{str(start.minute).zfill(2)}"
            return get_file(system, key)

        elif isinstance(system, systems.System):

            key = f"{system.system_code}.{str(start.year).zfill(4)}{str(start.month).zfill(2)}{str(start.day).zfill(2)}_{str(start.hour).zfill(2)}{str(start.minute).zfill(2)}"
            return get_file(system.system_code, key)
        
        elif isinstance(system, (list, dict, type(None))):

            files: Dict[str, File] = {}

            system = [] if not system else system
            
            # Iterate through system codes to fetch files
            for system_code in system.copy():
                
                key = f"{system_code}.{str(start.year).zfill(4)}{str(start.month).zfill(2)}{str(start.day).zfill(2)}_{str(start.hour).zfill(2)}{str(start.minute).zfill(2)}"
                file = get_file(system_code, key)

                if file:

                    files[system_code] = file
                    files[system_code].system = systems.get(system_code=system_code)
                    system.remove(system_code)
            
            if any(system):

                payload = {
                    "start": start,
                    "system_code[]": system
                }

                response = api_request(api_endpoint, payload)
                json_files = response.json()
                
                if json_files:
                    
                    if isinstance(json_files, dict):

                        json_files = [json_files]
                
                json_files = {file["system_code"]: file for file in json_files}
                
                for system_code, json_file in json_files.items():

                    key = f"{system_code}.{str(start.year).zfill(4)}{str(start.month).zfill(2)}{str(start.day).zfill(2)}_{str(start.hour).zfill(2)}{str(start.minute).zfill(2)}"
                    files[system_code] = File(*json_file.values())
                    files[system_code].system = systems.get(system_code=system_code)
                    Cache.cache(key, json.dumps(files[system_code], indent=4))
            
            return files if files else None

    try:

        start, end = parse(interval)
    
    except TypeError:

        return None

    if isinstance(system, (str, systems.System)):

        # Handle a single system or system code
        system = system if isinstance(system, str) else system.system_code
    
    elif isinstance(system, (list, dict, type(None))):
        
        if isinstance(system, dict):
            
            # If 'system' is a dict, extract system codes from its values
            system = [s.system_code for s in system.values()]

        elif isinstance(system, list):

            if isinstance(system[0], systems.System):

                system = [s.system_code for s in system]
        
        elif isinstance(system, NoneType):

            system = [system.system_code for system in systems.all().values()]


    if end:

        files: Dict[str, List[File]] = {}

        payload = {
            "from": start,
            "to": end,
            "system_code[]": system
        }

        response = api_request(api_endpoint, payload)

        for file in response.json():

            system_code = file.get("system_code")
            files.setdefault(system_code, []).append(File(*file.values()))

        return files
         
    else:

        return process(start, system)