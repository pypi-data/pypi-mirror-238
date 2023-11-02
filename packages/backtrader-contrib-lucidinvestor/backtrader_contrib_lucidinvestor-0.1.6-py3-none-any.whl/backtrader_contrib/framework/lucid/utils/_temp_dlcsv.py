from data_adjuster import DataBundle
import pathlib
import os

p = pathlib.Path(__file__).parent.parent.parent.resolve()
parent_bt_contrib = str(p).split('backtrader_contrib/backtrader_contrib')[0]
csv_path = os.path.join(parent_bt_contrib, 'data/as_traded')

symbols = ['TLH', 'ICF']

csv_path = pathlib.Path(__file__).parent
assets_list = ["AAPL"]  # reproduce quantopian analysis
data = DataBundle(assets_list=symbols)
