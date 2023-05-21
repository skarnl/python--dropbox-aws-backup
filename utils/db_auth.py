import sys
import os
import dropbox
import dotenv
import cache

dotenv.load_dotenv()

dropbox_app_key = os.getenv("DROPBOX_APP_KEY")
dropbox_app_secret = os.getenv("DROPBOX_APP_SECRET")

if not dropbox_app_key or not dropbox_app_secret:
    print("No client_id or client_secret found, provide one in the .env file")
    sys.exit()


def get_dropbox_client():
    # if the access_token exists, don't start the flow
    existing_access_token = cache.get_cached_token()

    if not existing_access_token:
        new_access_token = start_auth_flow()

        cache.store_token_in_cache(new_access_token)

    # store the access_token
    return dropbox.Dropbox(oauth2_access_token=cache.get_cached_token())


def start_auth_flow():
    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(
        consumer_key=dropbox_app_key,
        consumer_secret=dropbox_app_secret,
        token_access_type='legacy'
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

    return oauth_result.access_token
