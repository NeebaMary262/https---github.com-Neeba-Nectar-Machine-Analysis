
import pandas as pd
from datetime import datetime, timedelta
import configparser
from date.date_time import get_time_in_dubai
from lib.asset_history import get_asset_history, get_filtered_assets  # Adjust import based on your actual structure

def convert_epoch_to_datetime(epoch_time):
    return datetime.fromtimestamp(epoch_time / 1000.0)

def format_timedelta(delta):
    hours, remainder = divmod(delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"0 days {int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def calculate_working_hours(asset_history):
    records = []

    for asset in asset_history:
        asset_name = asset["source"]["data"]["displayName"]
        point_data = asset["pointData"][0]["values"]
        df = pd.DataFrame(point_data)
        df['dataTime'] = pd.to_datetime(df['dataTime'], unit='ms')
        df.sort_values(by='dataTime', inplace=True)

        durations = {"On": timedelta(), "Off": timedelta(), "Idle": timedelta()}
        prev_time = df['dataTime'].iloc[0]
        prev_status = df['data'].iloc[0]

        for i in range(1, len(df)):
            current_time = df['dataTime'].iloc[i]
            current_status = df['data'].iloc[i]
            duration = current_time - prev_time

            durations[prev_status] += duration

            prev_time = current_time
            prev_status = current_status

        last_time = df['dataTime'].iloc[-1]
        last_status = df['data'].iloc[-1]
        end_of_day = last_time.replace(hour=23, minute=59, second=59)
        last_duration = end_of_day - last_time
        durations[last_status] += last_duration

        # Calculate start of day for the first timestamp
        first_time = df['dataTime'].iloc[0]
        start_of_day = first_time.replace(hour=0, minute=0, second=0)
        first_duration = first_time - start_of_day
        first_status = df['data'].iloc[0]
        durations[first_status] += first_duration

        target_date = df['dataTime'].iloc[0].strftime('%Y-%m-%d')
        total_duration = sum(durations.values(), timedelta())

        records.append({
            'Asset': asset_name,
            'Date': target_date,
            'Operation Status On': format_timedelta(durations['On']),
            'Operation Status Off': format_timedelta(durations['Off']),
            'Operation Status Idle': format_timedelta(durations['Idle']),
            'Total Time Duration': format_timedelta(total_duration)
        })

    working_hours_df = pd.DataFrame(records)
    return working_hours_df

if __name__ == "__main__":
    # Load configuration
    config = configparser.ConfigParser()
    config.read('lib/config.properties')

    # Get the start and end times for yesterday in Dubai timezone
    start_time_epoch, end_time_epoch = get_time_in_dubai()

    # Retrieve filtered assets
    offset = int(config.get('nec-aws-stg', 'offset'))
    filtered_assets = get_filtered_assets(config, offset)

    if filtered_assets and "assets" in filtered_assets:
        asset_count = filtered_assets['totalAssetsCount']
        length = int(config.get('nec-aws-stg', 'pageSize'))
        num_of_pages = (asset_count + length - 1) // length  # Ensure rounding up for pagination

        for x in range(1, num_of_pages + 1):
            filtered_assets = get_filtered_assets(config, x)  # Pass config and x as parameters
            if filtered_assets and "assets" in filtered_assets:
                for asset in filtered_assets["assets"]:
                    # Get asset history for each asset one at a time
                    asset_history = get_asset_history(config, asset, start_time_epoch, end_time_epoch)
                    
                    if asset_history:
                        working_hours_df = calculate_working_hours(asset_history)

                        # Define the path for the CSV file
                        csv_file_path = 'D:/Machine_analysis/Analysis/runhours.csv'

                        # Save the DataFrame to a CSV file
                        working_hours_df.to_csv(csv_file_path, index=False, mode='a', header=not pd.io.common.file_exists(csv_file_path))


