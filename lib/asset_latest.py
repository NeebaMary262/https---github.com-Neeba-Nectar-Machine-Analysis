

import requests

from lib.login_api import login_to_api

def get_filtered_assets(config, offset):
    """
    Retrieve filtered assets from the API using the provided configuration.

    Args:
    - config: ConfigParser object containing configuration details.
    - offset: Offset for pagination.

    Returns:
    - filtered_assets: Filtered assets retrieved from the API.
    """
    try:
        # Get domain and page size from configuration
        domain = config.get('nec-aws-stg', 'domain')
        page_size = int(config.get('nec-aws-stg', 'pageSize'))

        # Construct URL for asset list endpoint
        url = config.get('nec-aws-stg', 'apihost') + config.get('nec-aws-stg', 'AssetListURL')

        # Retrieve access token using login_to_api function
        access_token = login_to_api(config)
       
        

        if access_token:
            # Set headers for the API request
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            # Prepare data for the API request
            data = {
                "domain": domain,
                "pageSize": page_size,
                "offset": offset,
                "order": "desc",
                "sortField": "dataTime"
            }

            # Make the API request to retrieve filtered assets
            response = requests.post(url, headers=headers, json=data)

            # Check if the request was successful
            if response.status_code == 200:
                # Retrieve filtered assets from the response
                filtered_assets = response.json()
                
                
                return filtered_assets
            else:
                # Handle error response
                print(f"Failed to retrieve filtered assets. Status code: {response.status_code}, Response: {response.text}")
                return None
        else:
            # Handle login failure
            print("Failed to retrieve access token.")
            return None
    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred while retrieving filtered assets: {e}")
        return None
