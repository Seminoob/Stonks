import pandas as pd
def marubuzo(data, perc=0.005, shift=1):
    df1 = data[(((data.High - data.Open) <= (data.Close*perc)) & ((data.Close - data.Low) <= data.Close*perc))]
    df1['bull_maru'] = 0
    for i in range(len(df1)):
        if data['Close'].iloc[df1.index[i] + 1] > df1['Close'].iloc[i]:
            df1['bull_maru'].iloc[i] = 1


    return df1