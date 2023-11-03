from __future__ import annotations
from .timestamps import Timestamps
import numpy as np
import datetime
import copy

class PPS:

    def __init__(self, index: np.ndarray, time: np.ndarray):

        self.index = index
        self.time = time
        self.timestamps = Timestamps(self.time)
        self.datetime = [datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=int(x)) for x in self.time]
        self.dt = np.diff(self.time)
        self.di = np.diff(self.index)

    
    def to_corrected_PPS(self, file_type: str) -> PPS:
        
        corrected_pps = copy.deepcopy(self)
        
        if file_type == "RSP2":
 
            indices = corrected_pps.index
            times = corrected_pps.timestamps.get_us()
            p = np.polyfit(indices, times - times[0], 1)
            
            new_timestamps = times[0] + np.polyval(p, indices)
            
            corrected_pps.timestamps.set_us([int(round(new_timestamp)) for new_timestamp in new_timestamps])
            
            corrected_pps.time = corrected_pps.timestamps.get_us()
            
        return corrected_pps