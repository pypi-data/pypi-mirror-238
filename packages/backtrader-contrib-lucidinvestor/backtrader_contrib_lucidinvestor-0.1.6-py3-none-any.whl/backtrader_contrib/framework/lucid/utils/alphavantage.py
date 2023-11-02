
from alpha_vantage.timeseries import TimeSeries

api_key = 'J59PAHV7T0P6G4Y6'
# Initialize the Alpha Vantage API client
ts = TimeSeries(key=api_key, output_format='pandas')

# Define the stock symbol and the time period (2014-01-01 to 2014-12-31)
symbol = 'AAPL'
start_date = '2014-01-01'
end_date = '2014-12-31'

# Get unadjusted price data
unadjusted_data, _ = ts.get_daily(symbol=symbol, outputsize='full')
unadjusted_data.to_csv("alpha_vantage_AAPL_all.csv")
unadjusted_data_2014 = unadjusted_data[(unadjusted_data.index >= start_date) & (unadjusted_data.index <= end_date)]

# Get adjusted price data
#adjusted_data, _ = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
#adjusted_data_2014 = adjusted_data[(adjusted_data.index >= start_date) & (adjusted_data.index <= end_date)]

# Print the data
print("Unadjusted Price Data for AAPL in 2014:")
print(f'May 15th: {unadjusted_data_2014["4. close"]["2014-05-15"]}')
print(f'May 30th: {unadjusted_data_2014["4. close"]["2014-05-30"]}')
print(f'June 9th: {unadjusted_data_2014["4. close"]["2014-06-09"]}')
print(f'June 13th: {unadjusted_data_2014["4. close"]["2014-06-13"]}')

print(f'2020-08-31: {unadjusted_data["4. close"]["2020-08-31"]}')
#print(f'1987-06-16: {unadjusted_data["4. close"]["1987-06-16"]}')



unadjusted_data_2014.to_csv("alpha_vantage_AAPL_2014.csv")

#print("\nAdjusted Price Data for AAPL in 2014:")
#print(adjusted_data_2014)