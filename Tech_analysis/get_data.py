import pandas_datareader.data as web
import pandas as pd


def data(ticker, start, end, source='yahoo', loc='stonk_dfs', name=None):
    if name is None:
        name = ticker
    df = web.DataReader(ticker, source, start, end)
    df.to_csv(loc + '/{}.csv'.format(name))