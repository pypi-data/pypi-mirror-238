import struct
import numpy as np
import io
from .signal import Signal

class Header:

    fmt_main = "<H 2d 2Q 5d 2H 5d 6s 6s 6s 234s"
    fmt_reserve = " 256s"
    fmt = fmt_main + fmt_reserve

    def __init__(self, buffer):
     
        (
            self.version,
            self.samplerate,
            self.lo_freq,
            self.start_us,
            self.pps_count,
            self.beacon_lat,
            self.beacon_long,
            self.beacon_alt,
            self.beacon_freq,
            self.beacon_power,
            self.beacon_polar,
            self.ant_id,
            self.ant_lat,
            self.ant_long,
            self.ant_alt,
            self.ant_az,
            self.ant_el,
            self.beacon_code,
            self.observer_code,
            self.station_code,
            self.description) = struct.unpack(
                                self.fmt_main,
                                buffer[0:struct.calcsize(self.fmt_main)]
                                )

    def pack(self):

        # Pack the values of instance variables into a binary buffer
        packed_data = struct.pack(
            self.fmt_main,
            self.version,
            self.samplerate,
            self.lo_freq,
            self.start_us,
            self.pps_count,
            self.beacon_lat,
            self.beacon_long,
            self.beacon_alt,
            self.beacon_freq,
            self.beacon_power,
            self.beacon_polar,
            self.ant_id,
            self.ant_lat,
            self.ant_long,
            self.ant_alt,
            self.ant_az,
            self.ant_el,
            self.beacon_code,
            self.observer_code,
            self.station_code,
            self.description
        )

        return packed_data + bytes(256)


class PPS:

    fmt = "Q Q"

    def __init__(self, buffer):

        self.pps = struct.unpack(
            self.fmt * int(len(buffer) / struct.calcsize(self.fmt)),
            buffer
        )

        self.index = np.array(self.pps[0::2])
        self.time = np.array(self.pps[1::2])

    def pack(self):

        return struct.pack(self.fmt * int(len(self.pps) / (struct.calcsize(self.fmt) / 8)), *self.pps)


class Data:

    def __init__(self, buffer, dtype: np.int16 | np.float64):

        self.dtype = dtype
        self.fmt = "h" if self.dtype == np.int16 else "d"
        self.npoints = int(len(buffer) / struct.calcsize(self.fmt))
        self.signal = np.array(struct.unpack("<" + self.fmt * self.npoints, buffer))

    def set(self, signal: Signal):

        self.dtype = signal.data.dtype
        self.fmt = "h" if self.dtype == np.int16 else "d"
        self.signal = signal.data
        self.npoints = len(self.signal)
        

    def pack(self):

        return struct.pack(self.fmt * len(self.signal), *self.signal)

class Wav:

    def __init__(self, buffer):

        self.buffer = buffer
        self.header, self.pps, self.data = self.read()
    
    def write(self):

        brams_header = self.header.pack()
        brams_pps = self.pps.pack()
        brams_data = self.data.pack()

        stream = io.BytesIO()

        # Write the RIFF header
        stream.write(b'RIFF')
        fmt_size = 16 if self.data.dtype == np.int16 else 18
        size = 36 + fmt_size + len(brams_header) + len(brams_data) + len(brams_pps)
        stream.write(struct.pack('<I', size))
        stream.write(b'WAVE')

        self.aformat = 1 if self.data.dtype == np.int16 else 3
        self.blockalign = 2 if self.data.dtype == np.int16 else 8
        self.bps = 16 if self.data.dtype == np.int16 else 64
        self.byterate = self.blockalign * self.channels * self.samplerate

        stream.write(b'fmt ')
        stream.write(struct.pack('<I', 16 if self.data.dtype == np.int16 else 18))
        stream.write(struct.pack('HHIIHH', self.aformat, self.channels, self.samplerate, self.byterate, self.blockalign, self.bps))
        stream.write(struct.pack("H", 0)) if self.data.dtype == np.float64 else None
        
        stream.write(b'BRA1')
        stream.write(struct.pack('<I', len(brams_header)))
        stream.write(brams_header)

        # Write the data chunk

        stream.write(b'data')
        stream.write(struct.pack('<I', len(brams_data)))
        stream.write(brams_data)

         # Write the BRA2 chunk (optional)
        if brams_pps is not None:
            
            stream.write(b'BRA2')
            stream.write(struct.pack('<I', len(brams_pps)))
            stream.write(brams_pps)

        # Get the stream contents as a byte string
        wav_data = stream.getvalue()

        return wav_data

    def read(self):

        brams_header = None
        brams_pps = None
        brams_data = None

        stream = io.BytesIO(self.buffer)

        riff, size, fformat = struct.unpack('<4sI4s', stream.read(12))

        chunk_header = stream.read(8)
        subchunkid, subchunksize = struct.unpack('<4sI', chunk_header)

        if subchunkid == b'fmt ':

            self.aformat, self.channels, self.samplerate, self.byterate, self.blockalign, self.bps= struct.unpack('HHIIHH', stream.read(16))
            stream.read(2) if self.aformat == 3 else None

        chunkOffset = stream.tell()

        while chunkOffset < size:

            stream.seek(chunkOffset)
            subchunkid, subchunksize = struct.unpack('<4sI', stream.read(8))

            if subchunkid == b'BRA1':
                
                if not (subchunksize == struct.calcsize(Header.fmt)):

                    return None

                brams_header = Header(stream.read(struct.calcsize(Header.fmt_main)))
    
            elif subchunkid == b'data':

                brams_data = Data(stream.read(subchunksize), np.int16 if self.aformat == 1 else np.float64)
                
            elif subchunkid == b'BRA2':

                brams_pps = PPS(stream.read(subchunksize))
            else:
                pass
            chunkOffset += (subchunksize + 8)

        return (brams_header, brams_pps, brams_data)