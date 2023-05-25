import sys
import os
import dropbox
import dotenv
import cache
from utils.colorize import colorize
from colorama import Fore

dotenv.load_dotenv()

dropbox_app_key = os.getenv("DROPBOX_APP_KEY")
dropbox_app_secret = os.getenv("DROPBOX_APP_SECRET")

if not dropbox_app_key or not dropbox_app_secret:
    print(colorize("No client_id or client_secret found, provide one in the .env file", Fore.RED))
    sys.exit()


def get_dropbox_client():
    # if the access_token exists, don't start the flow
    existing_token = cache.get_cached_token()

    if not existing_token:
        new_token = start_auth_flow()

        cache.store_token_in_cache(new_token)

    return dropbox.Dropbox(oauth2_refresh_token=cache.get_cached_token(), app_key=dropbox_app_key, app_secret=dropbox_app_secret)


def start_auth_flow():
    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(
        consumer_key=dropbox_app_key,
        consumer_secret=dropbox_app_secret,
        token_access_type='offline'
    )

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print('2. Click "Allow" (you might have to log in first).')
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        print("Error: %s" % (e,))
        sys.exit(1)

    print(oauth_result)

    return oauth_result.refresh_token


def refresh_client():
    print(colorize("Refresh client", Fore.CYAN))

    return get_dropbox_client()