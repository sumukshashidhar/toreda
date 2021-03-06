from datetime import date
from datetime import timedelta
import pandas as pd
import time
import logging
import os
logging.basicConfig(level=logging.DEBUG, filename='./logs/analysis/general.log', format='%(levelname)s:%(name)s:%(asctime)s:%(message)s', filemode='w')
logger = logging.getLogger()



"""
Constants Declaration
"""
KEYPATH = os.path.realpath('./keys/keys.pem')

"""
API - Key Reading and Writing Functions
"""


def read_keys():
    """
    Reads the keys from the specified KEYPATH and returns a dictionary of keys, along with unix timestamps of their use
    """
    keylist = []
    try:
        with open(KEYPATH, 'r') as f:
            keylist = f.readlines()
    except FileNotFoundError:
        logger.critical("Did not find the keyfile")
    keylist = [x.rstrip('\n') for x in keylist]
    logger.debug("Created the keylist.")
    d = {}
    for i in keylist:
        d[i] = 0
    return d


def select_one_key(keydb):
    """
    Returns the least recently used key in the current dictionary. This assists with high frequency data analysis.

    @params
    keydb = dictionary
    """
    cur_time = time.time()
    max_time = 0
    max_time_key = None
    for i in keydb.keys():
        if cur_time - keydb[i] > max_time:
            max_time_key = i
            max_time = cur_time - keydb[i]
    keydb[max_time_key] = cur_time
    return max_time_key, keydb


def intraday(ticker, interval, key):
    """
    Returns interday data
    """
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}&apikey={key}&datatype=csv'
    df = pd.read_csv(url)
    try:
        df = df.sort_values(by='timestamp')
    except KeyError:
        logger.critical(f'{ticker}-{interval}-{key}: Failed')
        time.sleep(5)
        df = pd.read_csv(url)
        logger.fatal(f'Waited 5 secs. Now checking again')
        df.sort_values(by='timestamp')
    df = df.reset_index()
    logger.info(f'Got the dataframe intraday using key {key}')
    flag = True
    ctr = 40
    while flag:
        try:
            ti = ' 23:' + str(ctr) + ':00'
            df = df.iloc[df[df['timestamp'] == str(str(date.today() - timedelta(days=1)) + ti)].index.values[0]:]
            flag = False
        except IndexError:
            # print(f'failed for {ctr} continuing')
            ctr += 1
            flag = True
            if ctr >= 60:
                flag = False
    return df


def interday(ticker, key):
    """
    Returns the timeseries values for interday trading (long range)
    """
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={key}&datatype=csv'
    df = pd.read_csv(url)
    logger.info(f'Got the dataframe interday using key {key}')
    return df





