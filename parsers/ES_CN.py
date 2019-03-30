#!/usr/bin/env python3

import logging

# The arrow library is used to handle datetimes
from arrow import get
# The request library is used to fetch content through HTTP
from requests import Session
from ree import (ElHierro, GranCanaria, Gomera, LanzaroteFuerteventura,
                 LaPalma, Tenerife)
from .lib.exceptions import ParserException
from .lib.validation import validate


# Minimum valid zone demand. This is used to eliminate some cases
# where generation for one or more modes is obviously missing.
FLOORS = {
    'ES-CN-FVLZ': 50,
    'ES-CN-GC': 150,
    'ES-CN-IG': 3,
    'ES-CN-LP': 10,
    'ES-CN-TE': 150,
    'ES-CN-HI': 2
}

# TODO: Remove verify SSL config when working without it.
def fetch_island_data(zone_key, session):
    if zone_key == 'ES-CN-FVLZ':
        lanzarote_fuerteventura_data = LanzaroteFuerteventura(session, verify=False).get_all()
        if not lanzarote_fuerteventura_data:
            raise ParserException(zone_key, "LanzaroteFuerteventura not response")
        else:
            return lanzarote_fuerteventura_data
    elif zone_key == 'ES-CN-GC':
        gran_canaria_data = GranCanaria(session, verify=False).get_all()
        if not gran_canaria_data:
            raise ParserException(zone_key, "GranCanaria not response")
        else:
            return gran_canaria_data
    elif zone_key == 'ES-CN-IG':
        gomera_data = Gomera(session, verify=False).get_all()
        if not gomera_data:
            raise ParserException(zone_key, "Gomera not response")
        else:
            return gomera_data
    elif zone_key == 'ES-CN-LP':
        la_palma_data = LaPalma(session, verify=False).get_all()
        if not la_palma_data:
            raise ParserException(zone_key, "LaPalma not response")
        else:
            return la_palma_data
    elif zone_key == 'ES-CN-TE':
        tenerife_data = Tenerife(session, verify=False).get_all()
        if not tenerife_data:
            raise ParserException(zone_key, "Tenerife not response")
        else:
            return tenerife_data
    elif zone_key == 'ES-CN-HI':
        el_hierro_data = ElHierro(session, verify=False).get_all()
        if not el_hierro_data:
            raise ParserException(zone_key, "ElHierro not response")
        else:
            return el_hierro_data
    else:
        raise ParserException(zone_key, 'Can\'t read this country code {0}'.format(zone_key))


def fetch_consumption(zone_key='ES-CN', session=None, target_datetime=None, logger=None):
    if target_datetime:
        raise NotImplementedError('This parser is not yet able to parse past dates')
    
    ses = session or Session()
    island_data = fetch_island_data(zone_key, ses)
    data = []
    for response in island_data:
        response_data = {
            'zoneKey': zone_key,
            'datetime': get(response.timestamp).datetime,
            'consumption': response.demand,
            'source': 'demanda.ree.es'
        }

        data.append(response_data)

    return data


def fetch_production(zone_key, session=None, target_datetime=None,
                     logger=logging.getLogger(__name__)):
    if target_datetime:
        raise NotImplementedError('This parser is not yet able to parse past dates')
    
    ses = session or Session()
    island_data = fetch_island_data(zone_key, ses)
    data = []

    if zone_key == 'ES-CN-HI':
        for response in island_data:
            if response.production() > 0:
                response_data = {
                    'zoneKey': zone_key,
                    'datetime': get(response.timestamp).datetime,
                    'production': {
                        'coal': 0.0,
                        'gas': round(response.gas + response.combined, 2),
                        'solar': round(response.solar, 2),
                        'oil': round(response.vapor + response.diesel, 2),
                        'wind': round(response.wind, 2),
                        'hydro': 0.0,
                        'biomass': 0.0,
                        'nuclear': 0.0,
                        'geothermal': 0.0
                    },
                    'storage': {
                        'hydro': round(-response.hydraulic, 2),
                        'battery': 0.0
                    },
                    'source': 'demanda.ree.es',
                }
                response_data = validate(response_data, logger,
                                         floor=FLOORS[zone_key])

                if response_data:
                    # append if valid
                    data.append(response_data)

    else:
        for response in island_data:
            if response.production() > 0:
                response_data = {
                    'zoneKey': zone_key,
                    'datetime': get(response.timestamp).datetime,
                    'production': {
                        'coal': 0.0,
                        'gas': round(response.gas + response.combined, 2),
                        'solar': round(response.solar, 2),
                        'oil': round(response.vapor + response.diesel, 2),
                        'wind': round(response.wind, 2),
                        'hydro': round(response.hydraulic, 2),
                        'biomass': 0.0,
                        'nuclear': 0.0,
                        'geothermal': 0.0
                    },
                    'storage': {
                        'hydro': 0.0,
                        'battery': 0.0
                    },
                    'source': 'demanda.ree.es',
                }
                response_data = validate(response_data, logger,
                                         floor=FLOORS[zone_key])

                if response_data:
                    # append if valid
                    data.append(response_data)

    return data


if __name__ == '__main__':
    session = Session
    print("# ES-CN-FVLZ")
    print(fetch_consumption('ES-CN-FVLZ', session))
    print(fetch_production('ES-CN-FVLZ', session))
    print("# ES-CN-GC")
    print(fetch_consumption('ES-CN-GC', session))
    print(fetch_production('ES-CN-GC', session))
    print("# ES-CN-IG")
    print(fetch_consumption('ES-CN-IG', session))
    print(fetch_production('ES-CN-IG', session))
    print("# ES-CN-LP")
    print(fetch_consumption('ES-CN-LP', session))
    print(fetch_production('ES-CN-LP', session))
    print("# ES-CN-TE")
    print(fetch_consumption('ES-CN-TE', session))
    print(fetch_production('ES-CN-TE', session))
    print("# ES-CN-HI")
    print(fetch_consumption('ES-CN-HI', session))
    print(fetch_production('ES-CN-HI', session))
