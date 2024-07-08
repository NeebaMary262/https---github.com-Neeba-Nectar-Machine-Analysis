

# import requests
# import configparser
# from lib.asset_latest import get_filtered_assets
# from lib.login_api import login_to_api


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'date')))

# from date.date_time import get_time_in_dubai
# import requests
# import configparser
# from lib.asset_latest import get_filtered_assets
# from lib.login_api import login_to_api
# from date.date_time import get_time_in_dubai

# def get_asset_history(config, asset, start_time_epoch, end_time_epoch):
#     """
#     Retrieve asset history from the API using the provided configuration and asset details.

#     Args:
#     - config: ConfigParser object containing configuration details.
#     - asset: Dictionary containing asset details.
#     - start_time_epoch: Start time in epoch format.
#     - end_time_epoch: End time in epoch format.

#     Returns:
#     - asset_history: Asset history data retrieved from the API.
#     """
#     try:
#         # Extract necessary details from the asset
#         asset_type = asset.get("type")
#         domain = asset.get("domain")
#         identifier = asset.get("identifier")

#         # Get API host and asset history URL from configuration
#         apihost = config.get('nec-aws-stg', 'apihost')
#         asset_history_url = config.get('nec-aws-stg', 'AssetHistoryURL')
#         url = apihost + asset_history_url

#         # Retrieve access token
#         access_token = login_to_api(config)

#         if access_token:
#             # Set headers for the API request
#             headers = {
#                 "Authorization": f"Bearer {access_token}",
#                 "Content-Type": "application/json"
#             }

#             # Prepare data for the API request
#             data = {
#                 "sources": [
#                     {
#                         "asset": {
#                             "type": asset_type,
#                             "data": {
#                                 "domain": domain,
#                                 "identifier": identifier
#                             }
#                         },
#                         "pointNames": [
#                             "Motion Status"
#                         ]
#                     }
#                 ],
#                 "startDate": start_time_epoch,
#                 "endDate": end_time_epoch
#             }

#             # Make the API request to retrieve asset history
#             response = requests.post(url, headers=headers, json=data)

#             # Check if the request was successful
#             if response.status_code == 200:
#                 # Retrieve asset history from the response
#                 asset_history = response.json()
#                 return asset_history
#             else:
#                 # Handle error response
#                 print(f"Failed to retrieve asset history. Status code: {response.status_code}, Response: {response.text}")
#                 return None
#         else:
#             # Handle login failure
#             print("Failed to retrieve access token.")
#             return None
#     except Exception as e:
#         # Handle any unexpected errors
#         print(f"An error occurred while retrieving asset history: {e}")
#         return None

# if __name__ == "__main__":
#     # Load configuration
#     config = configparser.ConfigParser()
#     config.read('config.properties')

#     # Retrieve filtered assets
#     offset = int(config.get('nec-aws-stg', 'offset'))
#     filtered_assets = get_filtered_assets(config, offset)

#     if filtered_assets and "assets" in filtered_assets:
#         asset_count = filtered_assets['totalAssetsCount']
#         length = int(config.get('nec-aws-stg', 'pageSize'))
#         num_of_pages = (asset_count + length - 1) // length  # Ensure rounding up for pagination

#         # Get the start and end times for yesterday in Dubai timezone
#         start_time_epoch, end_time_epoch = get_time_in_dubai()

#         for x in range(1, num_of_pages + 1):
#             filtered_assets = get_filtered_assets(config, x)  # Pass config and x as parameters
#             if filtered_assets and "assets" in filtered_assets:
#                 for asset in filtered_assets["assets"]:
#                     # Get asset history for each asset one at a time
#                     asset_history = get_asset_history(config, asset, start_time_epoch, end_time_epoch)
                    
#     else:
#         print("Failed to retrieve filtered assets or no assets found.")



import requests
import configparser
from lib.asset_latest import get_filtered_assets
from lib.login_api import login_to_api


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'date')))

from date_time import get_time_in_dubai

def get_asset_history(config, asset, start_time_epoch, end_time_epoch):
    """
    Retrieve asset history from the API using the provided configuration and asset details.

    Args:
    - config: ConfigParser object containing configuration details.
    - asset: Dictionary containing asset details.
    - start_time_epoch: Start time in epoch format.
    - end_time_epoch: End time in epoch format.

    Returns:
    - asset_history: Asset history data retrieved from the API.
    """
    try:
        asset_type = asset.get("type")
        domain = asset.get("domain")
        identifier = asset.get("identifier")

        apihost = config.get('nec-aws-stg', 'apihost')
        asset_history_url = config.get('nec-aws-stg', 'AssetHistoryURL')
        url = apihost + asset_history_url

        access_token = login_to_api(config)

        if access_token:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            data = {
                "sources": [
                    {
                        "asset": {
                            "type": asset_type,
                            "data": {
                                "domain": domain,
                                "identifier": identifier
                            }
                        },
                        "pointNames": [
                            "Motion Status"
                        ]
                    }
                ],
                "startDate": start_time_epoch,
                "endDate": end_time_epoch
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                asset_history = response.json()
                return asset_history
            else:
                print(f"Failed to retrieve asset history. Status code: {response.status_code}, Response: {response.text}")
                return None
        else:
            print("Failed to retrieve access token.")
            return None
    except Exception as e:
        print(f"An error occurred while retrieving asset history: {e}")
        return None

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('lib/config.properties')

    offset = int(config.get('nec-aws-stg', 'offset'))
    filtered_assets = get_filtered_assets(config, offset)

    if filtered_assets and "assets" in filtered_assets:
        asset_count = filtered_assets['totalAssetsCount']
        length = int(config.get('nec-aws-stg', 'pageSize'))
        num_of_pages = (asset_count + length - 1) // length

        start_time_epoch, end_time_epoch = get_time_in_dubai()

        for x in range(1, num_of_pages + 1):
            filtered_assets = get_filtered_assets(config, x)
            if filtered_assets and "assets" in filtered_assets:
                for asset in filtered_assets["assets"]:
                    asset_history = get_asset_history(config, asset, start_time_epoch, end_time_epoch)
                    print(asset_history)
        print("Failed to retrieve filtered assets or no assets found.")

