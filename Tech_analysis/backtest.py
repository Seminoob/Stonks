import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


def backtesting(data, cap = float(1000), max_share=1):
    positions = pd.DataFrame(index=data.index).fillna(0.0)
    portfolio = pd.DataFrame(index=data.index).fillna(0.0)
    positions['signal'] = data['signal'] * max_share
    portfolio['positions'] = positions.multiply(data['price'], axis=0)
    portfolio['cash'] = cap - positions.diff().multiply(data['price'], axis=0).cumsum()
    portfolio['total'] = portfolio['positions'] + portfolio['cash']
    return portfolio


def returns_plot(data, start_date=None, end_date = None):

    if start_date and end_date is not None:
        start_date = dt.datetime(2001, 1, 1)
        end_date = dt.datetime(2018, 1, 1)
        goog_data = data.loc[(data.index > start_date) & (data.index < end_date)]
    else:
        goog_data = data
    goog_monthly_return = goog_data['Adj Close'].pct_change().groupby(
        [goog_data['Adj Close'].index.year,
         goog_data['Adj Close'].index.month]).mean()
    goog_montly_return_list = []
    for i in range(len(goog_monthly_return)):
        goog_montly_return_list.append \
            ({'month': goog_monthly_return.index[i][1],
              'monthly_return': goog_monthly_return[i]})
    goog_montly_return_list = pd.DataFrame(goog_montly_return_list,
                                           columns=('month', 'monthly_return'))
    goog_montly_return_list.boxplot(column='monthly_return',
                                    by='month')
    ax = plt.gca()
    labels = [item.get_text() for item in ax.get_xticklabels()]
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticklabels(labels)
    ax.set_ylabel('GOOG return')
    plt.tick_params(axis='both', which='major', labelsize=7)
    plt.title("GOOG Monthly return 2001-2018")
    plt.suptitle("")
    plt.show()