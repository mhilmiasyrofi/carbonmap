#!/usr/bin/env python3

"""Parser for the Orkney Islands"""

import arrow
import dateutil
import logging
import requests
from bs4 import BeautifulSoup

# There is a 2MW storage battery on the islands.
# http://www.oref.co.uk/orkneys-energy/innovations-2/

TZ = 'Europe/London'
DATETIME_LINK = 'https://www.ssen.co.uk/ANM/'
GENERATION_LINK = 'https://www.ssen.co.uk/Sse_Components/Views/Controls/FormControls/Handlers/ActiveNetworkManagementHandler.ashx?action=graph&contentId=14973&_=1537467858726'

GENERATION_MAPPING = {"Live Demand": "Demand",
                      "Orkney ANM": "ANM Renewables",
                      "Non-ANM Renewable Generation": "Renewables"}


def get_json_data(session):
    """
    Requests json data and extracts generation information.
    Returns a dictionary.
    """
    s = session or requests.Session()
    req = s.get(GENERATION_LINK)
    raw_json_data = req.json()

    generation_data = raw_json_data['data']['datasets']

    production = {}
    for datapoint in generation_data:
        gen_type = datapoint['label']
        val = float(max(datapoint['data']))
        production[gen_type] = val

    for k in list(production.keys()):
        if k not in GENERATION_MAPPING.keys():
            # Get rid of unneeded keys.
            production.pop(k)

    return production


def get_datetime(session):
    """
    Extracts data timestamp from html and checks it's less than 2 hours old.
    Returns an arrow object.
    """
    s = session or requests.Session()
    req = s.get(DATETIME_LINK)
    soup = BeautifulSoup(req.text, 'html.parser')

    data_table = soup.find("div", {"class": "Widget-Base Widget-ANMGraph"})

    last_updated = data_table.find("div", {"class": "button"}).contents
    raw_dt = last_updated[-1].strip().split('  ', 1)[-1]
    naive_dt = arrow.get(raw_dt, 'DD MMMM YYYY HH:mm:ss')
    aware_dt = naive_dt.replace(tzinfo=dateutil.tz.gettz(TZ))

    current_time = arrow.now(TZ)
    diff = current_time - aware_dt

    if diff.total_seconds() > 7200:
        raise ValueError('Orkney data is too old to use, data is {} hours old.'.format(diff.total_seconds()/3600))

    return aware_dt.datetime


def fetch_production(zone_key='GB-ORK', session=None, target_datetime=None,
                     logger=logging.getLogger(__name__)):
    """
    Requests the last known production mix (in MW) of a given country
        Arguments:
        zone_key (optional) -- used in case a parser is able to fetch multiple countries
        session (optional)  -- request session passed in order to re-use an existing session
        Return:
        A dictionary in the form:
        {
          'zoneKey': 'FR',
          'datetime': '2017-01-01T00:00:00Z',
          'production': {
              'biomass': 0.0,
              'coal': 0.0,
              'gas': 0.0,
              'hydro': 0.0,
              'nuclear': null,
              'oil': 0.0,
              'solar': 0.0,
              'wind': 0.0,
              'geothermal': 0.0,
              'unknown': 0.0
          },
          'storage': {
              'hydro': -10.0,
          },
          'source': 'mysource.com'
        }
    """
    if target_datetime:
        raise NotImplementedError('This parser is not yet able to parse past dates')

    raw_data = get_json_data(session)
    raw_data.pop("Live Demand")

    mapped_data = {}
    mapped_data['unknown'] = raw_data.get("Orkney ANM", 0.0) + raw_data.get("Non-ANM Renewable Generation", 0.0)

    dt = get_datetime(session)

    data = {
      'zoneKey': zone_key,
      'datetime': dt,
      'production': mapped_data,
      'storage': {
          'battery': None,
      },
      'source': 'ssen.co.uk'
    }

    return data


def fetch_exchange(zone_key1, zone_key2, session=None, target_datetime=None, logger=logging.getLogger(__name__)):
    """Requests the last known power exchange (in MW) between two zones

    Arguments:
    zone_key1, zone_key2: specifies which exchange to get
    session (optional): request session passed in order to re-use an existing session
    target_datetime: the datetime for which we want production data. If not provided, we should
      default it to now. The provided target_datetime is timezone-aware in UTC.
    logger: an instance of a `logging.Logger`; all raised exceptions are also logged automatically

    Return:
    A dictionary in the form:
    {
      'sortedZoneKeys': 'CA-QC->US-NEISO',
      'datetime': '2017-01-01T00:00:00Z',
      'netFlow': 0.0,
      'source': 'mysource.com'
    }
    """
    sorted_zone_keys = '->'.join(sorted([zone_key1, zone_key2]))
    raw_data = get_json_data(session)
    dt = get_datetime(session)

    # +ve importing from mainland
    # -ve export to mainland
    total_generation = raw_data['Orkney ANM'] + raw_data['Non-ANM Renewable Generation']
    netflow = raw_data['Live Demand'] - total_generation

    data = {'netFlow': netflow,
            'datetime': dt,
            'sortedZoneKeys': sorted_zone_keys,
            'source': 'ssen.co.uk'}

    return data


if __name__ == '__main__':
    print('fetch_production() ->')
    print(fetch_production())
    print('fetch_exchange(GB, GB-ORK)')
    print(fetch_exchange('GB', 'GB-ORK'))
