from . import constants as const
from . import qty


def get_temp(height: qty.Distance) -> qty.Temperature:
    """
    Returns the temperature at a given height.

    Parameters
    ----------
    height: Distance
        Distance from the qty module, representing a height in meters.

    Returns
    -------
    Temperature
        Temperature from the qty module, representing a temperature in Kelvin.

    Examples
    --------
    >>> height = qty.Distance.Ft(35000)
    >>> atm.get_temp(height)
    218.808 K
    """

    temp_at_height = qty.Temperature(const.Atm.SL.temp - const.Atm.lapse_rate * height)

    return temp_at_height


def get_pressure(temp: qty.Temperature) -> qty.Pressure:
    """
    Returns the pressure at a given atmospheric temperature.

    Parameters
    ----------
    temp: Temperature
        Temperature from the qty module, represented in Kelvin.

    Returns
    -------
    Pressure
        Pressure from the qty module, represented in Pascal.

    Examples
    --------
    >>> temp = qty.Temperature(288.15)
    >>> atm.get_pressure(temp)
    101325.0 Pa
    """

    pressure_at_temp = const.Atm.SL.pressure * (temp / const.Atm.SL.temp) ** (
        const.Earth.gravity / (const.Atm.lapse_rate * const.Atm.r_air)
    )

    return qty.Pressure(pressure_at_temp)


def get_density(height: qty.Distance) -> float:
    """
    Returns the pressure at a given height.

    Parameters
    ----------
    height: Distance
        Distance from the qty module, representing a height in meters.

    Returns
    -------
    float
        Float value representing the air density in kg/m^3.

    Examples
    --------
    >>> height = qty.Distance.Ft(35000)
    >>> atm.get_density(height)
    0.379...
    """

    temp_at_height = get_temp(height)
    pressure_at_height = get_pressure(temp_at_height)
    density_at_height = pressure_at_height / (const.Atm.r_air * temp_at_height)

    return density_at_height
