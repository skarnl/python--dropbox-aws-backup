import os
import dropbox
import dotenv

dotenv.load_dotenv()

access_token = os.getenv('DROPBOX_ACCESS_TOKEN')

if not access_token:
    print('No access token found, provide one in the .env file')
    exit()

dbx = dropbox.Dropbox(access_token)
current_account = dbx.users_get_current_account()




def get_year_list():
    pass


# def get_photos(year, month):
#     pass

# get_years
# - per year:   get_months
# -- per month:
#  get_photos
#  zip_photos
#  generate_hash / checksum
#  upload_to_aws + verify checksum
#  delete photos + zip
#  -> next month
# -> next year

