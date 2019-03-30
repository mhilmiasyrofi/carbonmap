#!/usr/bin/env python3
# coding=utf-8
import logging
import datetime
import pandas as pd
# The arrow library is used to handle datetimes
import arrow
# The request library is used to fetch content through HTTP
import requests

from io import StringIO

# Abbreviations:
# JP-HKD : Hokkaido
# JP-TH  : Tohoku (incl. Niigata)
# JP-TK  : Tokyo area (Kanto)
# JP-CB  : Chubu
# JP-HR  : Hokuriku
# JP-KN  : Kansai
# JP-CG  : Chugoku
# JP-SK  : Shikoku
# JP-KY  : Kyushu
# JP-ON  : Okinawa


exchange_mapping = {
    'JP-HKD->JP-TH':[1],
    'JP-TH->JP-TK':[2],
    'JP-CB->JP-TK':[3],
    'JP-CB->JP-KN':[4],
    'JP-CB->JP-HR':[5,11],
    'JP-HR->JP-KN':[6],
    'JP-CG->JP-KN':[7],
    'JP-KN->JP-SK':[8],
    'JP-CG->JP-SK':[9],
    'JP-CG->JP-KY':[10]
    }


def fetch_exchange(zone_key1='JP-TH', zone_key2='JP-TK', session=None,
                   target_datetime=None, logger=logging.getLogger(__name__)):
    """
    Requests the last known power exchange (in MW) between two zones

    Arguments:
    ----------
    zone_key: used in case a parser is able to fetch multiple countries
    session: request session passed in order to re-use an existing session
    target_datetime: the datetime for which we want production data. If not
      provided, we should default it to now. If past data is not available,
      raise a NotImplementedError. Beware that the provided target_datetime is
      UTC. To convert to local timezone, you can use
      `target_datetime = arrow.get(target_datetime).to('America/New_York')`.
      Note that `arrow.get(None)` returns UTC now.
    logger: an instance of a `logging.Logger` that will be passed by the
      backend. Information logged will be publicly available so that correct
      execution of the logger can be checked. All Exceptions will automatically
      be logged, so when something's wrong, simply raise an Exception (with an
      explicit text). Use `logger.warning` or `logger.info` for information
      that can useful to check if the parser is working correctly. A default
      logger is used so that logger output can be seen when coding / debugging.

    Returns:
    --------
    If no data can be fetched, any falsy value (None, [], False) will be
      ignored by the backend. If there is no data because the source may have
      changed or is not available, raise an Exception.

    A dictionary in the form:
    {
      'sortedZoneKeys': 'DK->NO',
      'datetime': '2017-01-01T00:00:00Z',
      'netFlow': 0.0,
      'source': 'mysource.com'
    }
    """
    #get target date in time zone Asia/Tokyo
    query_date = arrow.get(target_datetime).to('Asia/Tokyo').strftime('%Y/%m/%d')
    #get d-1 in tz Asia/Tokyo
    query_date_1 = arrow.get(target_datetime).shift(days=-1).to('Asia/Tokyo').strftime('%Y/%m/%d')

    sortedZoneKeys = '->'.join(sorted([zone_key1, zone_key2]))
    exch_id = exchange_mapping[sortedZoneKeys]
    r = session or requests.session()
    # Login to occtonet
    Cookies = get_cookies(r)
    # Get headers for querying exchange
    Headers = get_headers(r, exch_id[0], query_date, Cookies)
    Headers_1 = get_headers(r, exch_id[0], query_date_1, Cookies)
    # Add request tokens to headers
    Headers = get_request_token(r, Headers, Cookies)
    Headers_1 = get_request_token(r, Headers_1, Cookies)
    # Query data
    data = get_exchange(r, Headers, Cookies)
    data_1 = get_exchange(r, Headers_1, Cookies)
    # Concatenate d-1 and current day
    df = pd.concat([data_1,data])
    # CB-HR -exceptions
    if sortedZoneKeys == 'JP-CB->JP-HR':

        df = df.set_index(['Date', 'Time'])

        Headers = get_headers(r, exch_id[1], query_date, Cookies)
        Headers_1 = get_headers(r, exch_id[1], query_date_1, Cookies)

        Headers = get_request_token(r, Headers, Cookies)
        Headers_1 = get_request_token(r, Headers_1, Cookies)

        data = get_exchange(r, Headers, Cookies)
        data_1 = get_exchange(r, Headers_1, Cookies)

        df2 = pd.concat([data_1,data])
        df2 = df2.set_index(['Date', 'Time'])

        df = df + df2
        df = df.reset_index()

    # fix occurrences of 24:00hrs
    list24 = list(df.index[df['Time']=='24:00'])
    for idx in list24:
        df.loc[idx, 'Date'] = arrow.get(df.loc[idx, 'Date']).shift(days=1).strftime('%Y/%m/%d')
        df.loc[idx, 'Time'] = '00:00'
    # correct flow direction, if needed
    flows_to_revert = ['JP-CB->JP-TK', 'JP-CG->JP-KN', 'JP-CG->JP-SK']
    if sortedZoneKeys in flows_to_revert:
        df['netFlow'] = -1 * df['netFlow']

    df['source'] = 'occtonet.occto.or.jp'
    df['datetime'] = df.apply(parse_dt, axis=1)

    df['sortedZoneKeys'] = sortedZoneKeys
    df = df[['source', 'datetime', 'netFlow', 'sortedZoneKeys']]

    results = df.to_dict('records')
    for result in results:
        result['datetime'] = result['datetime'].to_pydatetime()
    return results

def fetch_exchange_forecast(zone_key1='JP-TH', zone_key2='JP-TK', session=None,
                   target_datetime=None, logger=logging.getLogger(__name__)):
    """
    Gets exchange forecast between two specified zones.
    Returns a list of dictionaries.
    """
    #get target date in time zone Asia/Tokyo
    query_date = arrow.get(target_datetime).to('Asia/Tokyo').strftime('%Y/%m/%d')
    # Forecasts ahead of current date are not available
    if query_date > arrow.get().to('Asia/Tokyo').strftime('%Y/%m/%d'):
        raise NotImplementedError(
            "Future dates(local time) not implemented for selected exchange")

    sortedZoneKeys = '->'.join(sorted([zone_key1, zone_key2]))
    exch_id = exchange_mapping[sortedZoneKeys]
    # Login to occtonet
    r = session or requests.session()
    Cookies = get_cookies(r)
    Headers = get_headers(r, exch_id[0], query_date, Cookies)
    # Query data
    Headers = get_request_token(r, Headers, Cookies)
    df = get_exchange_fcst(r, Headers, Cookies)
    # CB-HR -exceptions
    if sortedZoneKeys == 'JP-CB->JP-HR':

        df = df.set_index(['Date', 'Time'])
        Headers = get_headers(r, exch_id[1], query_date, Cookies)
        Headers = get_request_token(r, Headers, Cookies)
        df2 = get_exchange_fcst(r, Headers, Cookies)
        df2 = df2.set_index(['Date', 'Time'])
        df = df + df2
        df = df.reset_index()

    # fix possible occurrences of 24:00hrs
    list24 = list(df.index[df['Time']=='24:00'])
    for idx in list24:
        df.loc[idx, 'Date'] = arrow.get(str(df.loc[idx, 'Date'])).shift(days=1).strftime('%Y/%m/%d')
        df.loc[idx, 'Time'] = '00:00'
    # correct flow direction, if needed
    flows_to_revert = ['JP-CB->JP-TK', 'JP-CG->JP-KN', 'JP-CG->JP-SK']
    if sortedZoneKeys in flows_to_revert:
        df['netFlow'] = -1 * df['netFlow']
    # Add zonekey, source
    df['source'] = 'occtonet.occto.or.jp'
    df['datetime'] = df.apply(parse_dt, axis=1)
    df['sortedZoneKeys'] = sortedZoneKeys
    df = df[['source', 'datetime', 'netFlow', 'sortedZoneKeys']]
    # Format output
    results = df.to_dict('records')
    for result in results:
        result['datetime'] = result['datetime'].to_pydatetime()
    return results

def get_cookies(session=None):
    s = session or requests.session()
    s.get('http://occtonet.occto.or.jp/public/dfw/RP11/OCCTO/SD/LOGIN_login')
    return s.cookies

def get_headers(session, exch_id, date, cookies):
    payload = {
            'ajaxToken':'',
            'downloadKey':'',
            'fwExtention.actionSubType':'headerInput',
            'fwExtention.actionType':'reference',
            'fwExtention.formId':'CA01S070P',
            'fwExtention.jsonString':'',
            'fwExtention.pagingTargetTable':'',
            'fwExtention.pathInfo':'CA01S070C',
            'fwExtention.prgbrh':'0',
            'msgArea':'',
            'requestToken':'',
            'requestTokenBk':'',
            'searchReqHdn':'',
            'simFlgHdn':'',
            'sntkTgtRklCdHdn':'',
            'spcDay':date,
            'spcDayHdn':'',
            'tgtRkl':'{:02d}'.format(exch_id),
            'transitionContextKey':'DEFAULT',
            'updDaytime':''
          }
    s = session
    r = s.post('http://occtonet.occto.or.jp/public/dfw/RP11/OCCTO/SD/CA01S070C?fwExtention.pathInfo=CA01S070C&fwExtention.prgbrh=0',
                   cookies=cookies, data=payload)
    headers=r.text
    headers = eval(headers.replace('false', 'False').replace('null', 'None'))
    if headers['root']['errMessage']:
        raise RuntimeError('Headers not available due to {}'.format(headers['root']['errMessage']))
    else:
        payload['msgArea'] = headers['root']['bizRoot']['header']['msgArea']['value']
        payload['searchReqHdn'] = headers['root']['bizRoot']['header']['searchReqHdn']['value']
        payload['spcDayHdn'] = headers['root']['bizRoot']['header']['spcDayHdn']['value']
        payload['updDaytime'] = headers['root']['bizRoot']['header']['updDaytime']['value']
    return payload

def get_request_token(session, payload, cookies):
    s = session
    payload['fwExtention.actionSubType']='ok'
    r = s.post('http://occtonet.occto.or.jp/public/dfw/RP11/OCCTO/SD/CA01S070C?'
               +'fwExtention.pathInfo=CA01S070C&fwExtention.prgbrh=0',
               cookies=cookies, data=payload)
    headers=r.text
    headers = eval(headers.replace('false', 'False').replace('null', 'None'))
    if headers['root']['errFields']:
        raise RuntimeError('Request token not available due to {}'.format(headers['root']['errFields']))
    else:
        payload['downloadKey'] = headers['root']['bizRoot']['header']['downloadKey']['value']
        payload['requestToken'] = headers['root']['bizRoot']['header']['requestToken']['value']
    return payload

def get_exchange(session, payload, cookies):
    s = session
    payload['fwExtention.actionSubType']='download'
    r = s.post('http://occtonet.occto.or.jp/public/dfw/RP11/OCCTO/SD/CA01S070C?'
               +'fwExtention.pathInfo=CA01S070C&fwExtention.prgbrh=0',
               cookies=cookies, data=payload)
    r.encoding = 'shift-jis'
    df = pd.read_csv(StringIO(r.text), delimiter=',')
    df = df[['対象日付', '対象時刻', '潮流実績']]
    df.columns = ['Date', 'Time', 'netFlow']
    df = df.dropna()
    return df

def get_exchange_fcst(session, payload, cookies):
    s = session
    payload['fwExtention.actionSubType']='download'
    r = s.post('http://occtonet.occto.or.jp/public/dfw/RP11/OCCTO/SD/CA01S070C?fwExtention.pathInfo=CA01S070C&fwExtention.prgbrh=0',
                   cookies=cookies, data=payload)
    r.encoding = 'shift-jis'
    df = pd.read_csv(StringIO(r.text), delimiter=',')
    df = df[['対象日付', '対象時刻', '計画潮流(順方向)']]
    df.columns = ['Date', 'Time', 'netFlow']
    df = df.dropna()
    return df

def parse_dt(row):
    return arrow.get(' '.join([row['Date'], row['Time']]).replace('/', '-')).replace(tzinfo='Asia/Tokyo').datetime

def zone_headers(zone, date):
    """
    Get query headers for querying intra-zone flows
    """
    area_map={
    'JP-HKD':1,
    'JP-TH':2,
    'JP-TK':3,
    'JP-CB':4,
    'JP-HR':5,
    'JP-KN':6,
    'JP-CG':7,
    'JP-SK':8,
    'JP-KY':9,
    'JP-ON':10
    }
    payload = {
            'ajaxToken':'',
            'areaCdAreaSumNon':'{:02d}'.format(area_map[zone]),
            'daPtn':'00',
            'daPtn1':'187',
            'daPtn2':'275',
            'daPtn3':'220',
            'daPtn4':'187',
            'daPtn5':'132',
            'downloadKey':'',
            'fwExtention.actionSubType':'headerInput',
            'fwExtention.actionType':'reference',
            'fwExtention.formId':'CB01S020P',
            'fwExtention.jsonString':'',
            'fwExtention.pagingTargetTable':'',
            'fwExtention.pathInfo':'CB01S020C',
            'fwExtention.prgbrh':'0',
            'msgArea':'',
            'requestToken':'',
            'requestTokenBk':'',
            'searchReqHdn':'',
            'table1.currentPage':'',
            'table1.dispRowNum':'200',
            'table1.endIndex':'',
            'table1.nextPageStartIndex':'',
            'table1.pagingMode':'editable',
            'table1.rows[0].rowParams.originRowIndex':'0',
            'table1.rows[0].rowParams.rowAddUpdate':'',
            'table1.rows[0].rowParams.rowDelete':'',
            'table1.rows[0].rowParams.rowNum':'',
            'table1.rows[0].rowParams.selected':'',
            'table1.startIndex':'',
            'table1.tableIdToken':'',
            'table1.totalPage':'',
            'tgtAreaHdn':'',
            'tgtDaHdn':'',
            'tgtNngp': date,
            'tgtNngpHdn':'',
            'transitionContextKey':'DEFAULT',
            'updDaytime':''
          }

    with requests.Session() as s:


        r = s.get('http://occtonet.occto.or.jp/public/dfw/RP11/OCCTO/SD/LOGIN_login')

    r2 = s.post('http://occtonet.occto.or.jp/public/dfw/RP11/OCCTO/SD/CB01S020C?fwExtention.pathInfo=CB01S020C&fwExtention.prgbrh=0',
                   cookies=s.cookies, data=payload)
    r2.encoding = 'utf-8'
    headers=r2.text
    headers = eval(headers.replace('false', 'False').replace('null', 'None'))
    return headers

def solve_flows(headers):
    """
    Solves flow equations for each node inside a zone for a given day,
    allowing possibly to add large isolated thermal generators, pump storages etc. to eMap
    Japanese regions in the future

    Expects a dictionary argument obtained by function zone_headers(zone, date)
    Returns net generation for each node at 30 minute intervals in a Pandas DataFrame
    """
    dict1 = headers['root']['bizRoot']['table']['table1']['table1']['rows']
    # For each transmission line:
    for entry in dict1:
        # Collect flows at each timestamp
        for i in range(1,49):
            column = 'colonLbl'+'{:02d}'.format((i*30)//60)+'{:02d}'.format((i*30)%60)
            try:
                entry[column] = entry[column]['value']
            except TypeError:
                pass
        # Collect line names
        if str(type(entry['flowHukuSeiHuku']))=="<class 'dict'>":
            entry['flowHukuSeiHuku'] = entry['flowHukuSeiHuku']['value']
        # Remove unneeded keys from dictionary for parsing it into DataFrame
        for key in ['daKv','rowParams.originRowIndex', 'rowParams.rowAddUpdate',
                   'rowParams.rowDelete', 'rowParams.rowNum', 'rowParams.selected',
                   'sdlNm']:
            try:
                del entry[key]
            except KeyError:
                pass
    # Format to DataFrame, with timestamps as rows
    df = pd.DataFrame(dict1).T
    df.columns = df.iloc[-1]
    df=df.drop(df.index[-1])

    df2 = pd.DataFrame()
    #Sum flows for each node
    for i in range(len(df.columns)):
        col = df.columns[i]
        src = col.split(' → ')[0]
        tgt = col.split(' → ')[-1]

        if src in df2.columns:
            df2[src] = df2[src]+pd.to_numeric(df.iloc[:,i])
        else:
            df2[src] = pd.to_numeric(df.iloc[:,i])

        if tgt in df2.columns:
            df2[tgt] = df2[tgt]-pd.to_numeric(df.iloc[:,i])
        else:
            df2[tgt] = -1*pd.to_numeric(df.iloc[:,i])
    timestamps = []
    # convert timestamps
    date = headers['root']['bizRoot']['header']['tgtNngp']['value']
    for ts in list(df2.index.values):
        time = headers['root']['bizRoot']['header'][ts]['label']
        timestamps.append(
            arrow.get('{0} {1}'.format(date, time).replace(
            '/', '-')).replace(tzinfo='Asia/Tokyo').datetime
        )
    df2 = df2.reset_index()
    df2['timestamps']=pd.Series(timestamps)
    df2=df2.set_index('timestamps')
    df2=df2.drop('index', axis=1)
    df2=df2.dropna()
    return df2



if __name__ == '__main__':
    """Main method, never used by the Electricity Map backend, but handy for testing."""

    print('fetch_exchange(JP-CB, JP-HR) ->')
    print(fetch_exchange('JP-CB', 'JP-HR')[-3:])
    print('fetch_exchange(JP-CG, JP-KY) ->')
    print(fetch_exchange('JP-CG', 'JP-KY')[-3:])
    print('fetch_exchange_forecast(JP-CB, JP-HR) ->')
    print(fetch_exchange_forecast('JP-CB', 'JP-HR')[-3:])
    print('fetch_exchange_forecast(JP-CG, JP-KY) ->')
    print(fetch_exchange_forecast('JP-CG', 'JP-KY')[-3:])
