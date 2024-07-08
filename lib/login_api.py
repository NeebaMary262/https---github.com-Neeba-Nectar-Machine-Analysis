# import requests

# def login():
#     # API endpoint
#     endpoint = "https://gge.nectarit.com:444/api/token/login"
    
#     # Input payload
#     payload = {
#         "userName": "support@gge",
#         "password": "HoneyBee@2025"
#     }
    
#     # Prepare the headers
#     headers = {
#         "Content-Type": "application/json"
#     }
    
#     # Make the API request
#     try:
#         response = requests.post(endpoint, json=payload, headers=headers)
#         response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
#         json_response = response.json()
#         return json_response
#     except requests.exceptions.RequestException as e:
#         print(f"Error logging in: {e}")
#         return None

# if __name__ == "__main__":
#     login_response = login()
#     if login_response:
#         print(login_response)


#         print("Login failed or encountered an error.")
import requests
import configparser

def get_config():
    # """
    # Read the configuration file and return the ConfigParser object.
    # """
    config = configparser.ConfigParser()
    config.read('config.properties')
    return config

def login_to_api(config):
 
    try:
        # Extract username, password, and login URL from the configuration
        username = config.get('nec-aws-stg', 'userName')
        password = config.get('nec-aws-stg', 'password')
        login_url = config.get('nec-aws-stg', 'LoginURL')

        # Set headers for the API request
        headers = {"Content-Type": "application/json"}

        # Prepare data for the API request
        data = {"userName": username, "password": password}

        # Make the API request
        response = requests.post(login_url, json=data, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Retrieve access token from the response
            access_token = response.json().get("accessToken")
            return access_token
        else:
            # Handle error response
            print(f"Failed to log in to the API. Status code: {response.status_code}, Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Error logging in: {e}")
        return None
    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred while logging in to the API: {e}")
        return None

if __name__ == "__main__":
    # Load configuration
    config = get_config()

    # Log in to the API and get the access token
    access_token = login_to_api(config)

    # Output the access token or handle the error
    if access_token:
        print(access_token)
    else:
        print("Login failed or encountered an error.")
