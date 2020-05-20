import pandas_datareader.data as web
import pandas as pd


def data(ticker, start, end, name=None):
    if name is None:
        name = ticker
    df = web.DataReader(ticker, 'yahoo', start, end)
    df.to_csv('stonk_dfs/{}.csv'.format(name))