import pandas as pd
import numpy as np

# Load the data
data = pd.read_csv('path_to_your_file.csv')
# Ensure the Date column is properly formatted as datetime
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# This function will forecast using Exponential Moving Average (EMA)
def forecast_ema(segment_data, span=12):
    """
    Compute the EMA for the given time series and forecast for the next 12 months.
    :param segment_data: The time series data of a particular segment
    :param span: The span of months for the EMA calculation
    :return: A DataFrame with the forecasts
    """
    # Calculate EMA
    ema = segment_data.ewm(span=span, adjust=False).mean()
    last_ema = ema.iloc[-1]
    
    # Forecast for the next 12 months
    forecasts = [last_ema] * 12  # Assumes a stable trend as per the last calculated EMA
    future_dates = pd.date_range(start=segment_data.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')
    forecast_df = pd.DataFrame(data=forecasts, index=future_dates, columns=['Forecast'])
    
    return forecast_df

# Prepare a DataFrame to collect all forecasts
all_forecasts = pd.DataFrame()

# Loop over each unique segment
for segment in data['Segment'].unique():
    segment_data = data[data['Segment'] == segment].copy()
    segment_data = segment_data[['Demand']]  # Assume 'Demand' is the column to forecast
    
    # Get the forecast data
    forecast_df = forecast_ema(segment_data['Demand'])
    forecast_df['Segment'] = segment  # Add a segment identifier
    
    # Append to the all_forecasts DataFrame
    all_forecasts = pd.concat([all_forecasts, forecast_df])

# Pivot the DataFrame to have segments as columns and Dates as index
all_forecasts.reset_index(inplace=True)
all_forecasts = all_forecasts.pivot(index='index', columns='Segment', values='Forecast')

# Print or save the consolidated forecast results
print(all_forecasts)

# Optional: Save to CSV
# all_forecasts.to_csv('forecast_results.csv')
