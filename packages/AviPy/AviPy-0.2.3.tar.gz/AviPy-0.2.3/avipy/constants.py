class Atm:
    class SL:
        pressure = 101325
        density = 1.2252
        temp = 288.15

    lapse_rate = 0.0065
    cp_air = 1005
    cv_air = 718
    r_air = cp_air - cv_air
    gamma_air = cp_air / cv_air


class Earth:
    """
    Contains variables related to our planet earth

    Attributes:
        radius [m]     The radius of planet earth in meters.
    """

    radius = 6378137
    "[m] Earth Radius"

    gravity = 9.81
    "[m/s^2] Earth gravitational acceleration"
