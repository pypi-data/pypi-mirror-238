# Copyright 2023 LucidInvestor <https://lucidinvestor.ca/>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

from backtrader_contrib.framework.lucid.utils.input_ouput import ImportHistoricalData
import os.path
import math
import time
import pandas_market_calendars as mcal
import backtrader_contrib as bt
import backtrader_contrib.analyzers as btanalyzers
import backtrader_contrib.observers as btobservers

# pyfolio showtime
# https://pyfolio.ml4trading.io/index.html
import warnings

warnings.filterwarnings('ignore')
import pyfolio as pf
from IPython.display import display
import matplotlib.pyplot as plt
from matplotlib import gridspec

# requires pip install tornado
# import matplotlib
# matplotlib.use('WebAgg')

import pandas as pd
import empyrical as ep


def common_sense_ratio(returns):
    """
    reference:
        This ratio was developed by Laurent Bernut
        https://www.quora.com/Under-what-market-conditions-does-mean-reversion-work-better-than-trend-following.
        It is the tail ratio * gain to pain ratio. A value greater than 1 implies the strategy has potential to
        be tradeable.

    :param returns:
    :return:
    """
    # common sense ratio
    ratio = (abs(returns.quantile(0.95)) * returns[returns > 0].sum()) / abs(
        abs(returns.quantile(0.05)) * returns[returns < 0].sum()
    )
    ratio = round(ratio, 2)
    return ratio


def plot_metrics(returns, ax):
    perf_stats_all = pf.timeseries.perf_stats(returns)
    csr = common_sense_ratio(returns=returns)
    perf_stats_all['Common Sense Ratio'] = csr

    metrics = [
        'Annual return', 'Cumulative returns', 'Annual volatility', 'Sharpe ratio', 'Calmar ratio', 'Sortino ratio',
        'Max drawdown', 'Skew', 'Kurtosis', 'Common Sense Ratio'
    ]

    _id = 1
    for met in range(len(metrics), 0, -1):
        metric_name = metrics[len(metrics) - met]
        ax.text(0.5, met, metric_name, fontsize=8, horizontalalignment='left')
        ax.text(9.5, met, round(perf_stats_all.loc[metric_name], 4), fontsize=8, horizontalalignment='right')

    ax.set_title('Performance', fontweight='bold')
    ax.grid(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.axis([0, 11, 0, 11])

    return ax


def plot_pf(pyfoliozer, benchmark_rets, live_start_date):
    """
    reference:
        https://www.blackarbs.com/blog/a-dead-simple-2-asset-portfolio-that-crushes-the-sampp500-part-3

    :param returns:
    :return:
    """

    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

    # aligning benchmark_rets on returns in case it spans a shorter timeframe
    benchmark_rets = benchmark_rets[benchmark_rets.index.isin(returns.index)]
    # similarly aligning ret,pos,trans,g_l on benchmark_rets in case it spans a shorter timeframe
    returns = returns[returns.index.isin(benchmark_rets.index)]
    positions = positions[positions.index.isin(returns.index)]

    # transactions and gross_lev indexes are set to start at 9:00, disregarding returns indexes.
    # todo: fix transactions, gross_lev indexes to match that of returns.
    # transactions = transactions[transactions.index.isin(returns.index)]
    # gross_lev = gross_lev[gross_lev.index.isin(returns.index)]

    print(f"\n Gross Leverage analysis. {gross_lev.describe()}")
    if max(gross_lev) > 1 or min(gross_lev) < 0:
        print(f"\n Portfolio activities were performed with leveraged. Check if this was intentional.")

    plots = [
        pf.plot_rolling_returns,
        pf.plot_drawdown_underwater,
        pf.plot_annual_returns,
        pf.plot_monthly_returns_heatmap,
        pf.plot_monthly_returns_dist,
    ]

    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(3, 3, height_ratios=[1.0, 1, 1])

    for i, func in enumerate(plots):

        if i == 0:
            ax = plt.subplot(gs[0, 0:2])
            # pf.plot_drawdown_periods(returns=returns, ax=ax)
            # pf.plotting.plot_rolling_returns(returns, benchmark_rets, live_start_date='2010-05-01')

            # cone: Determines the upper and lower bounds of an n standard deviation
            # cone of forecasted cumulative returns. Future cumulative mean and
            # standard deviation are computed by repeatedly sampling from the
            # in-sample daily returns (i.e. bootstrap). This cone is non-parametric,
            # meaning it does not assume that returns are normally distributed.
            pf.plot_rolling_returns(returns=returns,
                                    factor_returns=benchmark_rets,
                                    live_start_date=live_start_date,
                                    cone_std=(1.0, 1.5, 2.0),
                                    ax=ax
                                    )
            ax = plt.subplot(gs[0, 2:3])
            plot_metrics(returns, ax)
            # pf.plot_perf_stats(returns=returns, factor_returns=benchmark_rets, ax=ax)

        elif i == 1:
            ax = plt.subplot(gs[1, 0:2])
            func(returns, ax=ax)
            ax = plt.subplot(gs[1, 2:3])
            pf.plot_rolling_sharpe(returns)

        elif i <= 4:
            ax = plt.subplot(gs[2, i - 2])
            func(returns, ax=ax)

    plt.tight_layout()


def run_backtest(trading_strategy, update_target, start_date, end_date, datadir, yahoo=False,
                 plot_pyfolio=False, plot_bt_default=True, print_pyfolio=False, stdstats=True,
                 live_start_date=None, strategy_param=None, **kwargs):
    """
    run_backtest
    :return:
    """

    # Create a calendar
    exchange_calendar = 'NYSE'
    nyse = mcal.get_calendar(exchange_calendar)
    mytz = nyse.tz.zone
    _valid = nyse.schedule(start_date=start_date, end_date=end_date, tz=mytz)
    # update input start & end date to match trading days
    start_date = _valid.iloc[0]['market_open']
    end_date = _valid.iloc[-1]['market_open']

    live_start_date = pd.Timestamp(live_start_date, tz=mytz)

    # stdstats: https://www.backtrader.com/docu/observers-and-statistics/observers-and-statistics/
    cerebro = bt.Cerebro(stdstats=stdstats)
    # TODO: only if daily
    cerebro.broker.set_coc(True)  # match a Market order to the closing price of the bar in which the order was issued.
    cerebro.broker.set_checksubmit(checksubmit=True)  # check margin/cash before accepting an order into the system

    # get data from csv
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)

    historical_data = ImportHistoricalData(start_date, end_date, tz='America/New_York')
    for asset in update_target.assets.items():
        symbol = asset[1].symbol.upper()

        path = os.path.join(parentDir, datadir, symbol)
        path = path + '.csv'

        d1 = None
        if yahoo:
            d1 = historical_data.historical_yahoo(symbol)
        else:
            #d1 = historical_data.custom_csv(path)
            d1 = bt.feeds.YahooFinanceCSVData(dataname=path,
                                              fromdate=start_date.date(),
                                              todate=end_date.date(),
                                              adjclose=True,
                                              reverse=False)
            # datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
            # , fromdate=fromdate, todate=todate)

        # Add the Data Feed to Cerebro
        cerebro.adddata(d1, name=symbol)

    # Set our desired cash start
    startcash = 10000
    cerebro.broker.setcash(startcash)
    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addstrategy(strategy=trading_strategy, **strategy_param,
                        update_target=update_target.assets, **kwargs)

    # Analyzer
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydd')
    cerebro.addanalyzer(bt.analyzers.Returns)

    if print_pyfolio or plot_pyfolio:
        cerebro.addanalyzer(btanalyzers.PyFolio, _name='pyfolio')

    # Observers
    cerebro.addobserver(btobservers.DrawDown)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Run over everything
    thestrats = cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # print the analyzers
    firstStrat = thestrats[0]
    cagr = firstStrat.analyzers.returns.get_analysis()['rnorm100']
    sharpe = firstStrat.analyzers.mysharpe.get_analysis()['sharperatio']
    dd = firstStrat.analyzers.mydd.get_analysis()['max']['drawdown']
    moneydd = firstStrat.analyzers.mydd.get_analysis()['max']['moneydown']

    try:
        print(f"CAGR: {cagr:.2f}%\nSharpe: {sharpe:.3f} \nMax Drawdown: {dd:.2f}% - Money down: ${moneydd:.2f}")
    except:  # yes - broad exit!
        exit("\n >> There was an error getting the analyzers value. Verify if cerebro.run() executed trades.")

    if print_pyfolio or plot_pyfolio:
        pyfoliozer = firstStrat.analyzers.getbyname('pyfolio')

    if print_pyfolio:
        try:
            # sudo apt install python3-tk
            returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
            print('Annualised volatility of the portfolio = {:.4}'.format(pf.timeseries.annual_volatility(returns)))
            drawdown_df = pf.timeseries.gen_drawdown_table(returns, top=5)
            print(drawdown_df)
            print(pf.timeseries.perf_stats(returns))
            monthly_ret_table = ep.aggregate_returns(returns, 'monthly')
            monthly_ret_table = monthly_ret_table.unstack().round(3)
            ann_ret_df = pd.DataFrame(ep.aggregate_returns(returns, 'yearly'))
            ann_ret_df = ann_ret_df.unstack().round(3)
            print(monthly_ret_table)
            print(ann_ret_df)
        except:  # yes - broad exit!
            exit(
                "\n >> There was an error getting the pyfolio analyzers value. Verify if cerebro.run() executed trades "
                "or if pyfolio is correctly installed.")

    if plot_bt_default:
        cerebro.plot()

    if plot_pyfolio:

        bench_symb = 'SPY'
        if yahoo:
            bench = ImportHistoricalData(start_date, end_date)
            benchmark_rets = bench.historical_yahoo(bench_symb, csv_fmt=True)
            benchmark_rets = benchmark_rets.close.pct_change()
        else:
            # Simulate the header row isn't there if noheaders requested
            skiprows = 0
            header = 0
            path = os.path.join(parentDir, datadir, bench_symb)
            path = path + '.csv'
            dataframe = None
            dataframe = pd.read_csv(path,
                                    skiprows=skiprows,
                                    header=header,
                                    parse_dates=True,
                                    index_col=0
                                    )
            dataframe = dataframe.drop("Close", axis=1)
            dataframe.rename(
                columns={'Adj Close': 'close', 'Volume': 'volume', 'Low': 'low', 'High': 'high', 'Open': 'open'},
                inplace=True)
            dataframe.index.rename('date', inplace=True)
            benchmark_rets = dataframe.close.pct_change()

        # Daily return values for the first date cannot be calculated. Set these to zero.
        benchmark_rets[0] = 0
        benchmark_rets = benchmark_rets.tz_localize('UTC', level=0)
        benchmark_rets.rename(bench_symb, inplace=True)

        if (live_start_date - start_date).days < 0:
            print(f" \n\n !!! INPUT ERROR - \n the provided live_start_date of {str(live_start_date)} if "
                  f"before the start date of {str(start_date)}. Automatically switching to the mid point of the total "
                  f"period. \n\n")
            live_start_date = None

        # if nothing has been defined as the go-live date for out-of-sample testing
        if live_start_date is None:
            # get the mid date of the period by adding half the number of days to start date
            nb_trading_days = (end_date - start_date).days
            live_start_date = start_date + pd.DateOffset(days=math.floor(nb_trading_days / 2))

        plot_pf(pyfoliozer=pyfoliozer, benchmark_rets=benchmark_rets,
                live_start_date=live_start_date)
        plt.show()

    print("\n ######################")
    print(" INFO -- REMOVE CHEAT-ON-CLOSE IF NOT DAILY")

    ret = {
        "balance/start": startcash,
        "balance/end": cerebro.broker.getvalue(),
        "sharpe": firstStrat.analyzers.mysharpe.get_analysis(),
        "drawdown": firstStrat.analyzers.mydd.get_analysis()
    }

    return ret
