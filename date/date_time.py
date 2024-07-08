

from datetime import datetime, timedelta
import pytz
# def convert_epoch_to_datetime(epoch_time):
#     # Convert epoch time to struct_time
#     return datetime.datetime.fromtimestamp(epoch_time / 1000.0)
# def get_time_in_dubai():
#     dubai_tz = pytz.timezone("Asia/Dubai")
#     now_utc = datetime.now(pytz.utc)
#     now_dubai = now_utc.astimezone(dubai_tz)
#     start_of_yesterday = now_dubai - timedelta(days=1)
#     start_of_yesterday = start_of_yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
#     end_of_yesterday = now_dubai - timedelta(days=1)
#     end_of_yesterday = end_of_yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

#     start_time_epoch = int(start_of_yesterday.timestamp() * 1000)
#     end_time_epoch = int(end_of_yesterday.timestamp() * 1000)

#     return start_time_epoch, end_time_epoch
def get_time_in_dubai():
    dubai_tz = pytz.timezone("Asia/Dubai")
    now_dubai = datetime.now(dubai_tz)  # Directly get the current time in Dubai
    start_of_yesterday = now_dubai - timedelta(days=1)
    start_of_yesterday = start_of_yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_yesterday = now_dubai - timedelta(days=1)
    end_of_yesterday = end_of_yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    start_time_epoch = int(start_of_yesterday.timestamp() * 1000)
    end_time_epoch = int(end_of_yesterday.timestamp() * 1000)

    return start_time_epoch, end_time_epoch

