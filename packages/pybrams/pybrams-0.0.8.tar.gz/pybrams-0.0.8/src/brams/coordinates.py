from __future__ import annotations
from dataclasses import dataclass
from math import cos, radians, sin, sqrt
from typing import Any, Dict
import numpy as np
import json_fix # type: ignore

GRS80 = 6378.137, 298.257222100882711
WGS84 = 6378.137, 298.257223563


@dataclass
class GeodeticCoordinates:

    latitude: float
    longitude: float
    altitude: float

    def __json__(self) -> Dict[str, Any]:

        return self.__dict__

    def __add__(self, o: GeodeticCoordinates) -> GeodeticCoordinates:

        return GeodeticCoordinates(self.latitude + o.latitude, self.longitude + o.longitude, self.altitude + o.altitude)

    def __sub__(self, o: GeodeticCoordinates) -> GeodeticCoordinates:

        return GeodeticCoordinates(self.latitude - o.latitude, self.longitude - o.longitude, self.altitude - o.altitude)


@dataclass
class CartesianCoordinates:

    x: float
    y: float
    z: float

    def __json__(self) -> Dict[str, float]:

        return self.__dict__

    def __add__(self, o: CartesianCoordinates) -> CartesianCoordinates:

        return CartesianCoordinates(self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o: CartesianCoordinates) -> CartesianCoordinates:

        return CartesianCoordinates(self.x - o.x, self.y - o.y, self.z - o.z)


DOURBES_GEODETIC_COORDINATES = GeodeticCoordinates(50.097569, 4.588487, 0.167)


@dataclass
class Coordinates:

    geodetic: GeodeticCoordinates
    geocentric: CartesianCoordinates
    dourbocentric: CartesianCoordinates

    def __json__(self) -> Dict[str, GeodeticCoordinates | CartesianCoordinates]:

        return self.__dict__

    @staticmethod
    def geodetic2Geocentric(coordinates: GeodeticCoordinates) -> CartesianCoordinates:

        φ = radians(coordinates.latitude)
        λ = radians(coordinates.longitude)
        sin_φ = sin(φ)
        a, rf = WGS84           # semi-major axis, reciprocal flattening
        e2 = 1 - (1 - 1 / rf) ** 2  # eccentricity squared
        n = a / sqrt(1 - e2 * sin_φ ** 2)  # prime vertical radius
        # perpendicular distance from z axis
        r = (n + coordinates.altitude) * cos(φ)
        x = r * cos(λ)
        y = r * sin(λ)
        z = (n * (1 - e2) + coordinates.altitude) * sin_φ

        return CartesianCoordinates(x, y, z)

    @staticmethod
    def geodetic2Dourbocentric(geodetic: GeodeticCoordinates) -> CartesianCoordinates:

        DOURBES_GEOCENTRIC_COORDINATES = Coordinates.geodetic2Geocentric(DOURBES_GEODETIC_COORDINATES)

        φ = radians(geodetic.latitude)
        λ = radians(geodetic.longitude)

        translated = Coordinates.geodetic2Geocentric(geodetic) - DOURBES_GEOCENTRIC_COORDINATES

        C1 = np.array([translated.x, translated.y, translated.z])

        # Rotation around Dzd with an angle lon
        RotMatPhi = np.array([
            [cos(λ), sin(λ), 0],
            [-sin(λ), cos(λ), 0],
            [0, 0, 1]
        ])

        C2 = RotMatPhi @ C1

        # Rotation around Dyd with an angle lat
        RotMatPhi = np.array([
            [cos(φ), 0, sin(φ)],
            [0, 1, 0],
            [-sin(φ), 0, cos(φ)]
        ])

        C3 = RotMatPhi @ C2

        return CartesianCoordinates(C3[1], C3[2], C3[0])

    @classmethod
    def fromGeodetic(cls, latitude: float, longitude: float, altitude: float) -> Coordinates:

        geodeticCoordinates = GeodeticCoordinates(
            latitude, longitude, altitude)
        geocentricCoordinates = cls.geodetic2Geocentric(geodeticCoordinates)
        dourbocentricCoordinates = cls.geodetic2Dourbocentric(
            geodeticCoordinates)

        return cls(geodeticCoordinates, geocentricCoordinates, dourbocentricCoordinates)
