LucidInvestor
=============

`LUCID <https://lucidinvestor.ca/>`_ is a social platform that helps individual investors who want to control their
financial lives, to collectively analyze the real life results of investment strategies, and turn self-managed
portfolios into personalized automated trading systems.

With an `Open Core based on Backtrader <https://gitlab.com/algorithmic-trading-library>`_, anyone can
review public strategies source code, backtest and run them live on either `LUCID <https://lucidinvestor.ca/>`_ or
a self-managed Backtrader solutions.

    note: a self-managed Backtrader solutions means that it's one's responsibility to code all software necessary
    to manage and orchestrate all aspects of trading orders flow and execution on top of Backtrader.

Portfolio Strategies
---------------------

Implementations of Limited Model Portfolio ("LMP") are available in the sub-module
`backtrader_contrib/strategies/lucid </backtrader_contrib/strategies/lucid>`__.

The LucidInvestor Platform directly implements these open source strategies, implementing the necessary methods
overloading to manage and orchestrate all aspects of live trading orders flow and execution on top of Backtrader.

*LMP* are a subset of model portfolios that are well-researched, broadly published and easily accessible to investors;
LMP have the particularity to be limited to class of investors (not tailored to an individual), class of assets, and
industry sectors, without referencing specific securities or issuers.

Usage
-----

As simple as:

.. code-block:: python

  import backtrader_contrib as bt
  from backtrader_contrib.framework.lucid.strategy_generic import StrategyGeneric

  class MyStrategy(StrategyGeneric):
  ....

Example
********

Refer to
`fixed_target_allocation.py </backtrader_contrib/strategies/lucid/strategic_asset_allocation/fixed_target_allocations.py>`__.

.. image:: /backtrader_contrib/strategies/lucid/strategic_asset_allocation/60-40.png
   :width: 400
   :alt: 60-40 portfolio backtest on daily data.

Getting involved
----------------

contact us at info@lucidinvestor.ca

Open source licensing info
--------------------------
`BSD 3-Clause <LICENSE.bsd3>`__

.. include:: LICENSE.bsd3