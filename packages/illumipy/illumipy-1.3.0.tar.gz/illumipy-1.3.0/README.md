**illumipy** is a Python module for estimating outside Illumination levels for given location, date and time.
Requires an OpenWeatherMap API-key (see: https://openweathermap.org/appid)

## Current limitations:
- cloud level, sunrise and sunset are not available for dates in the past. Results might therefore be unreliable. Times for sunrise and sunset will always be for the current day.
- at 100% cloud coverage, Results might be unreliable.

## USAGE:
This package can be used via import function in Python or be run directly as a script with CLI options: 
### Import
To use the module, simply import illumipy and call the function
data.light_data(): This returns a dictionary object with
the following information:
+ ['illuminance']: Outside Brightness in Lux
+ ['time']: Time used as %-H (e.g. 4 or 12)
+ ['date']: Date used as YYYY-MM-DD
+ ['city']: City Used
+ ['country']: Country Used
+ ['cloud_coverage']: Cloud coverage in %
+ ['et_illuminance']: Extraterrestrial Illuminance in Lux
+ ['direct_illuminance']: Direct Illuminance in Lux
+ ['horizontal_illuminance']: Horizontal Illuminance in Lux
+ ['horizontal_sky_illuminance']: Horizontal Sky Illuminance in Lux
+ ['sunrise']: Time of Sunrise as hh:mm
+ ['sunset']: Time of sunset as hh:mm
+ ['sun_altitude']: Sund altitude at [Time] in degrees.
+ ['day']: True if there is daylight at [Time].
+ ['clear_sky_index'] = Aproximation of Clear Sky Index based on cloud coverage
+ ['cs_irradiance'] = Estimated Clear Sky Irradiance in W/m^2 based on solar altitude.
+ ['irradiance'] = Estimated current Irradiance in W/m^2 based on solar altitude and cloud coverage.
+ coverage.
+ ['air_mass'] = calculated air mass for given solar altitude, based on empirical model.
+ ['azimuth'] = Calculated solar azimuth for given time and location.
+ ['declination'] = calculated solar declination angle for given date.
+ ['LSTM'] = Local standard time meridian in degrees.
+ ['EOT'] = Equation of Time.

It Takes the following arguments:
+ time: str=[0-24], date: str=[YYYY-MM-DD], city: str=['City'], country: str=['Country'], api_key: str=['api_key'], cloud_coverage: int=[0-100]  

if no arguments are provided, defaults to values defined in defaults.py.
### Command line 
To use as script with CLI run <python -m illumipy>.
To get a list of available CLI options run <python -m illumipy -h>


Requirements:
- Python3
- Python packages:
  - requests
  - logging
  - math
  - sys
  - datetime
  - argparse
- OpenWeatherMap API-Key

Author: Kalle Fornia  
GitHub: https://github.com/duckwilliam/illumipy  
PyPi: https://pypi.org/project/illumipy  
Version: 1.3.0
10/2023