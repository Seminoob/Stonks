import pandas as pd
import numpy as np
import indicators


class ThreeSupertrend:
    def __init__(self, data, trend_ema_tp=100, ema_tp=20, atr_tps=(39, 1, 15),  mults=(5, 2, 1)):
        self.stock_data = data
        self.data = pd.DataFrame()
        self.atr_tps = atr_tps
        self.mults = mults
        for i in range(3):
            self.data['s{}'.format(i + 1)] = indicators.SuperTrend(self.stock_data, atr_tp=atr_tps[i],
                                                                   mult=mults[i]).data['SuperTrend']
        self.data['small_ema'] = indicators.Ma(data, tp=ema_tp, type='ema')
        self.data['trend_ema'] = indicators.Ma(data, tp=trend_ema_tp, type='ema')

