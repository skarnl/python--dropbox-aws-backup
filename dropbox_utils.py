import os
import dropbox
import dotenv
import cache

dotenv.load_dotenv()

dropbox_client_id = os.getenv("DROPBOX_CLIENT_ID")
dropbox_client_secret = os.getenv("DROPBOX_CLIENT_SECRET")

if not dropbox_client_id or not dropbox_client_secret:
    print("No client_id or client_secret found, provide one in the .env file")
    exit()


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
        dropbox_client_id,
        dropbox_client_secret,
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
        exit(1)

    print(oauth_result)

    return oauth_result.access_token
