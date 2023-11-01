"""
weather helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import logging
import math
import hub.helpers.constants as cte


class Weather:
  """
  Weather class
  """

  _epw_file = {
    'CA.02.5935': 'https://energyplus-weather.s3.amazonaws.com/north_and_central_america_wmo_region_4/CAN/BC/CAN_BC_Summerland.717680_CWEC/CAN_BC_Summerland.717680_CWEC.epw',
    'CA.10.06': 'https://energyplus-weather.s3.amazonaws.com/north_and_central_america_wmo_region_4/CAN/PQ/CAN_PQ_Montreal.Intl.AP.716270_CWEC/CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw',
    'CA.10.13': 'https://energyplus-weather.s3.amazonaws.com/north_and_central_america_wmo_region_4/CAN/PQ/CAN_PQ_Montreal.Intl.AP.716270_CWEC/CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw',
    'CA.10.14': 'https://energyplus-weather.s3.amazonaws.com/north_and_central_america_wmo_region_4/CAN/PQ/CAN_PQ_Montreal.Intl.AP.716270_CWEC/CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw',
    'CA.10.16': 'https://energyplus-weather.s3.amazonaws.com/north_and_central_america_wmo_region_4/CAN/PQ/CAN_PQ_Montreal.Intl.AP.716270_CWEC/CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw',
    'DE.01.082': 'https://energyplus-weather.s3.amazonaws.com/europe_wmo_region_6/DEU/DEU_Stuttgart.107380_IWEC/DEU_Stuttgart.107380_IWEC.epw',
    'US.NY.047': 'https://energyplus-weather.s3.amazonaws.com/north_and_central_america_wmo_region_4/USA/NY/USA_NY_New.York.City-Central.Park.94728_TMY/USA_NY_New.York.City-Central.Park.94728_TMY.epw',
    'CA.10.12': 'https://energyplus-weather.s3.amazonaws.com/north_and_central_america_wmo_region_4/CAN/PQ/CAN_PQ_Quebec.717140_CWEC/CAN_PQ_Quebec.717140_CWEC.epw',
    'IL.01.': 'https://energyplus-weather.s3.amazonaws.com/europe_wmo_region_6/ISR/ISR_Eilat.401990_MSI/ISR_Eilat.401990_MSI.epw'
  }
  # todo: this dictionary need to be completed, a data science student task?

  @staticmethod
  def sky_temperature(ambient_temperature):
    """
    Get sky temperature from ambient temperature in Celsius
    :return: List[float]
    """
    # Swinbank - Source sky model approximation(1963) based on cloudiness statistics(32 %) in the United States
    # ambient temperatures( in °C)
    # sky temperatures( in °C)
    values = []
    for temperature in ambient_temperature:
      value = 0.037536 * math.pow((temperature + cte.KELVIN), 1.5) \
              + 0.32 * (temperature + cte.KELVIN) - cte.KELVIN
      values.append(value)
    return values

  @staticmethod
  def cold_water_temperature(ambient_temperature):
    """
    Get cold water temperature from ambient temperature in Celsius
    :return: dict
    """
    # Equation from "TOWARDS DEVELOPMENT OF AN ALGORITHM FOR MAINS WATER TEMPERATURE", 2004, Jay Burch
    # and Craig Christensen, National Renewable Energy Laboratory
    # ambient temperatures( in °C)
    # cold water temperatures( in °C)
    ambient_temperature_fahrenheit = []
    average_temperature = 0
    maximum_temperature = -1000
    minimum_temperature = 1000
    for temperature in ambient_temperature:
      value = temperature * 9 / 5 + 32
      ambient_temperature_fahrenheit.append(value)
      average_temperature += value / 8760
      if value > maximum_temperature:
        maximum_temperature = value
      if value < minimum_temperature:
        minimum_temperature = value
    delta_temperature = maximum_temperature - minimum_temperature
    ratio = 0.4 + 0.01 * (average_temperature - 44)
    lag = 35 - 1 * (average_temperature - 44)
    cold_temperature = []
    for temperature in ambient_temperature_fahrenheit:
      radians = (0.986 * (temperature-15-lag) - 90) * math.pi / 180
      cold_temperature.append((average_temperature + 6 + ratio * (delta_temperature/2) * math.sin(radians) - 32) * 5/9)
    return cold_temperature

  def epw_file(self, region_code):
    """
    returns the url for the weather file for the given location or default (Montreal data)
    :return: str
    """
    if region_code not in self._epw_file:
      logging.warning('Specific weather data unknown for %s using Montreal data instead', region_code)
      return self._epw_file['CA.10.06']
    return self._epw_file[region_code]
