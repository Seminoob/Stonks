import pandas as pd
import numpy as np
from .indicators import SuperTrend, Ma
import matplotlib.pyplot as plt


class ThreeSupertrend:
    def __init__(self, data, trend_ema_tp=100, ema_tp=20, atr_tps=(39, 1, 15),  mults=(5, 2, 1)):
        self.stock_data = data
        self.data = pd.DataFrame()
        self.data['Close'] = self.stock_data['Close']
        self.atr_tps = atr_tps
        self.mults = mults
        for i in range(3):
            self.data['s{}'.format(i + 1)] = SuperTrend(self.stock_data, atr_tp=atr_tps[i],
                                                        mult=mults[i]).data['SuperTrend']
            print('s{} Calculated'.format(i + 1))
        self.small_ema = Ma(self.stock_data['Close'], tp=ema_tp, typ='ema')
        print('{} Ema Calculated'.format(ema_tp))
        self.trend_ema = Ma(self.stock_data['Close'], tp=trend_ema_tp, typ='ema')
        print('{} Ema Calculated'.format(trend_ema_tp))
        self.data['small_ema'] = self.small_ema.ma
        self.data['trend_ema'] = self.trend_ema.ma

    def generate_signal(self):
        self.data['signal'] = 0
        self.data.loc[(self.data['s2'] < self.stock_data['Close']) & (self.data['s3'] < self.stock_data['Close'])
                      & (self.data['small_ema'] < self.stock_data['Close']), 'signal'] = 1
        self.data['signal1'] = 0
        self.data.loc[self.data['signal'].diff() == 1, 'signal1'] = 1
        print('Signal Generated')

    def plot_signal(self, ax, ax2):
        ax.plot(self.stock_data['Date'].values, self.stock_data['Close'].values, color='b')
        ax.plot(self.stock_data['Date'].values, self.data['s1'].values, color='r')
        ax.plot(self.stock_data['Date'].values, self.data['s2'].values, color='r')
        ax.plot(self.stock_data['Date'].values, self.data['s3'].values, color='r')
        ax.plot(self.stock_data['Date'].values, self.data['small_ema'].values, color='k')
        ax.xaxis_date()
        ax2.plot(self.stock_data['Date'].values, self.data['signal'].values)
        ax2.set_ylim([0, 2])
        ax2.xaxis_date()