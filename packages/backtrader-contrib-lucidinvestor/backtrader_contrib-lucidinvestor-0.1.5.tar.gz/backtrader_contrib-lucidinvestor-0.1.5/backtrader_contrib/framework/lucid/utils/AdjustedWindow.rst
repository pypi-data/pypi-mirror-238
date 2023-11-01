Introducing the notion of adjusted time window, which provides the value of an OHLCV for a specific
asset at a specific window of times, adjusted for corporate events at that specific time.

Problem
-------

1. Split adjustments are typically applied to all prices and volumes before the algorithm even started.

2. This adjustment caused slippage and commissions to sometimes be slightly inaccurate, and also permitted some look-ahead bias to leak into the simulation

3. Yahoo adjusted change every day (eventually) - making reproducibility close to impossible, because a simulation tomorrow might use different adjustments than a simulation run today

Objective:

      backtesting should be reproducible.

      backtesting and live trading, should be able to match. Specifically,  You can now make accurate calculations of
      the returns of securities because the price information in the lookback window is fully adjusted.

Considerations:

* Price adjustments depend on three elements: the date of the price, the date that the price is being considered from,
  and any events (splits, dividends, and mergers) that happened between those two dates.
* Lookback windows should use prices that are split-, merger-, and dividend- adjusted to the date of simulation, or
  the latest date in the lookback should that not be the date of simulation.
* trading signals should be calculated on lookback-specific as-the-time adjusted Close for splits and dividends

Solution
--------

We created data_adjuster, containing the notion of:

**DataBundle class**, for which you have to pass a list of assets (from csv file or fetched from yahoo as a
testing strategy), and provides easy access to all necessary classes to `get_adjusted_window()`, and
`get_begining_of_month_adjusted_window()`.

**History class** that returns pandas.df of *as traded prices* and *time-window adjusted close prices*, with
possibilities to adjust for a date-specific window, or assuming that the end of the window is the day before the
current simulation time.

**SlidingWindow class** which supports calendar-based request for a sized window of data using
`pandas_market_calendars`. It also holds the desired lookback window (if any) > History inherits from SW