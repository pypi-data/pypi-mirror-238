import math
from typing import Literal

from . import constants as const
from . import qty


class Coord:
    __lat = None
    __lon = None

    def __init__(self, lat: float, lon: float, unit: Literal["deg", "rad"] = "deg"):
        self.set_lat(lat, unit)
        self.set_lon(lon, unit)

    def __repr__(self):
        return f"lat: {self.__lat}, lon: {self.__lon}"

    def __str__(self):
        return f"Latitude: {self.__lat:.2f}°, Longitude: {self.__lon:.2f}°"

    def set_lat(self, lat: float, unit: Literal["deg", "rad"] = "deg") -> "Coord":
        """
        Sets the latitude of the coordinate
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if unit.lower() == "rad":
            lat = math.degrees(lat)

        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be in range [-90, 90]")

        self.__lat = lat

        return self

    def set_lon(self, lon: float, unit: Literal["deg", "rad"] = "deg") -> "Coord":
        """
        Sets the longitude of the coordinate
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if unit.lower() == "rad":
            lon = math.degrees(lon)

        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be in range [-180, 180]")

        self.__lon = lon

        return self

    def get_lat(self, unit: Literal["deg", "rad"] = "deg") -> float:
        """
        Returns the latitude of the coordinate.

        Parameters
        ----------
        unit: "deg" or "rad", default "deg"
            Unit of measurement for latitude.

        Returns
        -------
        float

        Examples
        --------
        >>> coord = Coord(40, 50)
        >>> coord.get_lat()
        40
        >>> coord.get_lat("rad")
        0.698...
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if unit == "rad":
            return math.radians(self.__lat)

        return self.__lat

    def get_lon(self, unit: Literal["deg", "rad"] = "deg") -> float:
        """
        Returns the longitude of the coordinate.

        Parameters
        ----------
        unit: "deg" or "rad", default "deg"
            Unit of measurement for longitude.

        Returns
        -------
        float

        Examples
        --------
        >>> coord = Coord(40, 50)
        >>> coord.get_lat()
        50
        >>> coord.get_lat("rad")
        0.872...
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if unit == "rad":
            return math.radians(self.__lon)

        return self.__lon

    def get_latlon(self, unit: Literal["deg", "rad"] = "deg") -> tuple[float, float]:
        """
        Returns the latitude and longitude of the coordinate.

        Parameters
        ----------
        unit: "deg" or "rad", default "deg"
            Unit of measurement for latitude and longitude.

        Returns
        -------
        tuple of (lat, lon)

        Examples
        --------
        >>> coord = Coord(40, 50)
        >>> coord.get_latlon()
        (40, 50)
        >>> coord.get_latlon("rad")
        (0.698..., 0.872...)
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if unit == "rad":
            return (math.radians(self.__lat), math.radians(self.__lon))

        return (self.__lat, self.__lon)

    def isclose(self, coord: "Coord", tolerance: float = 0.5) -> bool:
        """
        Returns whether the coordinate is close the given other coordinate.

        Parameters
        ----------
        coord: Coord
            Other coordinate of which the closeness is compared to.
        tolerance: float between 0.1 and 10, default 0.5
            Tolerance of closeness in degrees of lat/lon.


        Returns
        -------
        Boolean

        Examples
        --------
        >>> coord1 = (0, 0)
        >>> coord2 = (2, 3)
        >>> coord1.isclose(coord2, tolerance=2)
        False
        >>> coord1.isclose(coord2, tolerance=3)
        True
        """
        lat, lon = coord.get_latlon()

        if tolerance < 0.1 or tolerance > 10:
            raise ValueError("Tolerance is not in range [0, 10]")

        if (lat - tolerance < self.__lat < lat + tolerance) and (lon - tolerance < self.__lon < lon + tolerance):
            return True
        return False

    def get_distance(self, coord: "Coord") -> qty.Distance:
        """
        Return meters of distance to the given point.

        Parameters
        ----------
        coord: Coord
            The coordinate to which the distance should be calculated.

        Returns
        -------
        Distance
            From the qty module, represents value in meters.

        Examples
        --------
        >>> coord1 = Coord(0, 0)
        >>> coord2 = Coord(0, 90)
        >>> coord1.get_distance(coord2)
        10018754.17 meters

        Source
        ------
        https://www.movable-type.co.uk/scripts/latlong.html
        """
        lat1, lon1 = self.get_latlon("rad")
        lat2, lon2 = coord.get_latlon("rad")

        delta_lon = lon2 - lon1

        distance = (
            math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(delta_lon))
            * const.Earth.radius
        )

        return qty.Distance(distance)

    def get_bearing(self, coord: "Coord") -> qty.Distance:
        """
        Returns the inital bearing to the given point.

        Parameters
        ----------
        coord: Coord
            The coordinate to which the bearing should be calculated.

        Returns
        -------
        float
            Float value representing the bearing in degrees.

        Examples
        --------
        >>> coord1 = Coord(0, 0)
        >>> coord2 = Coord(0, 90)
        >>> coord1.get_bearing(coord2)
        90.0

        Source
        ------
        https://www.movable-type.co.uk/scripts/latlong.html
        """
        lat1, lon1 = self.get_latlon("rad")
        lat2, lon2 = coord.get_latlon("rad")

        y = math.sin(lon2 - lon1) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)

        bearing_rad = math.atan2(y, x)
        bearing_deg = (math.degrees(bearing_rad) + 360) % 360

        return bearing_deg

    def get_next_coord(self, dist: qty.Distance, bearing_deg: float) -> "Coord":
        """
        Returns the a coordinate that is a given amount of meters away from that point, maintaining the given bearing.

        Parameters
        ----------
        dist: Distance
            Distance value from the qty module, represented in meters.
        bearing_deg: float
            Bearing to the next coordinate in degrees.

        Returns
        -------
        Coord

        Examples
        --------
        >>> coord1 = Coord(0, 0)
        >>> distance = qty.Distance(10000)
        >>> bearing = 180
        >>> coord1.get_next_coord(distance, bearing)
        Latitude: -89.83°, Longitude: 0.00°

        Source
        ------
        https://www.movable-type.co.uk/scripts/latlong.html
        """

        lat1, lon1 = self.get_latlon("rad")
        bearing = math.radians(bearing_deg)
        angular_dist = dist / const.Earth.radius

        lat2 = math.asin(
            math.sin(lat1) * math.cos(angular_dist) + math.cos(lat1) * math.sin(angular_dist) * math.cos(bearing)
        )

        lon2 = lon1 + math.atan2(
            math.sin(bearing) * math.sin(angular_dist) * math.cos(lat1),
            math.cos(angular_dist) - math.sin(lat1) * math.sin(lat2),
        )

        return Coord(lat2, lon2, unit="rad")
