import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


class Ma:
    def __init__(self, data, tp=10, mins=-1, typ='sma'):
        if mins == -1:
            self.mins = tp
        else:
            self.mins = mins
        self.tp = tp
        self.data = data
        if typ == 'ema':
            self.ma = self.data.ewm(span=tp, min_periods=mins).mean()
        elif typ == 'std':
            self.ma = self.data.rolling(window=tp, min_periods=mins).std()
        else:
            self.ma = self.data.rolling(window=tp, min_periods=mins).mean()

    def plotit(self, ax):
        ax.plot(self.data.iloc[:, 0].values, self.ma.values)
        ax.xaxis_date()


class Macd:
    def __init__(self, data, big=26, small=12, middle=9):
        self.stock_data = data
        self.data = pd.DataFrame()
        self.data['big_ema'] = self.stock_data.iloc[:, 1].ewm(span=big, min_periods=big).mean()
        self.data['small_ema'] = self.stock_data.iloc[:, 1].ewm(span=small, min_periods=small).mean()
        self.data['middle_ema'] = (self.data['big_ema'] - self.data['small_ema']).ewm(span=middle, min_periods=middle).mean()

    def plotit(self, ax):
        ax.plot(self.stock_data['Date'].values, self.data[['big_ema', 'small_ema']].values)
        ax.xaxis_date()
        ax3 = ax.twinx()
        ax3.bar(self.stock_data['Date'].values, self.data['middle_ema'].values, color=(self.data['middle_ema'] > 0).map({True: 'g', False: 'r'}))


class Atr:
    def __init__(self, data, tp=10):
        self.stock_data = data
        self.data = pd.DataFrame()
        self.data['hl'] = self.stock_data['High'] - self.stock_data['Low']
        self.data['chpc'] = self.stock_data['High'] - self.stock_data['Close'].shift()
        self.data['clpc'] = self.stock_data['Low'] - self.stock_data['Close'].shift()
        self.data['tr'] = self.data[['hl', 'chpc', 'clpc']].max(axis=1)
        self.data['atr'] = self.data['tr'].ewm(span=tp, min_periods=tp).mean()

    def plotit(self, ax):
        ax.plot(self.stock_data['Date'].values, self.data['atr'].values)
        ax.xaxis_date()

# FINAL UPPERBAND = IF( (Current BASICUPPERBAND  < Previous FINAL UPPERBAND) and
#                       (Previous Close > Previous FINAL UPPERBAND))
#                       THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
#
# FINAL LOWERBAND = IF( (Current BASIC LOWERBAND  > Previous FINAL LOWERBAND) and
# (Previous Close < Previous FINAL LOWERBAND))
# THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)
#
# SUPERTREND = IF(Current Close <= Current FINAL UPPERBAND )
# THEN Current FINAL UPPERBAND ELSE Current  FINAL LOWERBAND


class SuperTrend:
    def __init__(self, data, atr_tp=10, mult=3):
        self.stock_data = data
        self.data = pd.DataFrame()
        self.data['atr'] = Atr(self.stock_data, tp=atr_tp).data['atr']
        self.data['bub'] = ((self.stock_data['High'] + self.stock_data['Low']) / 2) + (mult * self.data['atr'])
        self.data['blb'] = ((self.stock_data['High'] + self.stock_data['Low']) / 2) - (mult * self.data['atr'])
        self.data['fub'] = self.data['bub']
        self.data['flb'] = self.data['blb']
        self.data['SuperTrend'] = np.nan

        for i in range(atr_tp, len(self.data.index)):
            if (self.data['bub'].iloc[i] < self.data['fub'].iloc[i - 1]) or (
                    self.stock_data['Close'].iloc[i - 1] > self.data['fub'].iloc[i - 1]):
                self.data['fub'].iloc[i] = self.data['bub'].iloc[i]
            else:
                self.data['fub'].iloc[i] = self.data['fub'].iloc[i - 1]
            if (self.data['blb'].iloc[i] > self.data['flb'].iloc[i - 1]) or (
                    self.stock_data['Close'].iloc[i - 1] < self.data['flb'].iloc[i - 1]):
                self.data['flb'].iloc[i] = self.data['blb'].iloc[i]
            else:
                self.data['flb'].iloc[i] = self.data['flb'].iloc[i - 1]
            if i == atr_tp:
                if self.data['fub'].iloc[atr_tp] > self.stock_data['Close'].iloc[atr_tp]:
                    self.data['SuperTrend'].iloc[atr_tp] = self.data['fub'].iloc[atr_tp]
                else:
                    self.data['SuperTrend'].iloc[atr_tp] = self.data['flb'].iloc[atr_tp]
            else:
                if self.data['SuperTrend'].iloc[i - 1] == self.data['fub'].iloc[i - 1]:
                    if self.stock_data['Close'].iloc[i] <= self.data['fub'].iloc[i]:
                        self.data['SuperTrend'].iloc[i] = self.data['fub'].iloc[i]
                    else:
                        self.data['SuperTrend'].iloc[i] = self.data['flb'].iloc[i]
                elif self.data['SuperTrend'].iloc[i - 1] == self.data['flb'].iloc[i - 1]:
                    if self.stock_data['Close'].iloc[i] >= self.data['flb'].iloc[i]:
                        self.data['SuperTrend'].iloc[i] = self.data['flb'].iloc[i]
                    else:
                        self.data['SuperTrend'].iloc[i] = self.data['fub'].iloc[i]

    def plotit(self, ax):
        green = np.ma.masked_where(self.data['SuperTrend'] < self.stock_data['Close'], self.data['SuperTrend'])
        red = np.ma.masked_where(self.data['SuperTrend'] >= self.stock_data['Close'], self.data['SuperTrend'])

        ax.plot(self.stock_data['Date'].values, green, self.stock_data['Date'].values, red)
        ax.xaxis_date()


class Rsi:
    def __init__(self, data, tp=14, type='sma'):
        self.stock_data = data
        self.data = pd.DataFrame()
        self.data['Diff'] = self.stock_data['Close'] - self.stock_data['Close'].shift()
        self.data['Gain'] = self.data['Diff'].where(self.data['Diff'] > 0, other=0)
        self.data['Loss'] = (self.data['Diff'].where(self.data['Diff'] < 0, other=0))*-1
        # self.data['Avg Gain'] = Ma(self.data[['Date', 'Gain']], tp=tp, type=type).ma
        # self.data['Avg Loss'] = Ma(self.data[['Date', 'Loss']], tp=tp, type=type).ma
        # self.data['RSI'] = 100 - (100 / (1 + (self.data['Avg Gain'] / self.data['Avg Loss'])))
        self.data['Avg Gain'] = 0
        self.data['Avg Loss'] = 0
        self.data.loc[tp, 'Avg Gain'] = self.data['Gain'].iloc[:tp].mean()
        self.data.loc[tp, 'Avg Loss'] = self.data['Loss'].iloc[:tp].mean()

        for i in range(tp + 1, len(self.data.index)):
            self.data.loc[i, 'Avg Gain'] = ((self.data.loc[i - 1, 'Avg Gain'] * 13) + self.data.loc[i, 'Gain']) / 14
            self.data.loc[i, 'Avg Loss'] = ((self.data.loc[i - 1, 'Avg Loss'] * 13) + self.data.loc[i, 'Loss']) / 14
        self.data['Rsi'] = 100 - (100 / (1 + (self.data['Avg Gain'] / self.data['Avg Loss'])))
    def plotit(self, ax):
        ax.plot(self.stock_data['Date'].values, self.data['Rsi'].values)
        ax.xaxis_date()
