import os
import dropbox_utils

BASE_PHOTO_FOLDER_PATH = "/fotos"
TEMP_FOLDER = "./__temp_folder__"

YEARS = [
    "2007-en-ervoor",
    # "2008",
    # "2009",
    # "2010",
    # "2011",
    # "2012",
    # "2013",
    # "2014",
    # "2015",
    # "2016",
    # "2017",
    # "2018",
    # "2019",
    # "2020",
    # "2021",
]

dbx = dropbox_utils.get_dropbox_client()

if not dbx:
    print("No dropbox client to work with")
    exit()


def clear_temp_dir():
    for root, dirs, files in os.walk(TEMP_FOLDER):
        for file in files:
            file_to_remove = os.path.join(root, file)

            print("Remove :" + file_to_remove)
            os.remove(file_to_remove)


def check_temp_exists():
    if os.path.exists(TEMP_FOLDER):
        print("Empty TEMP folder")
        clear_temp_dir()
    else:
        print("Create TEMP folder")
        os.makedirs(TEMP_FOLDER)


def get_files_list(year):

    list_folder_result = dbx.files_list_folder(path=BASE_PHOTO_FOLDER_PATH + "/" + year)
    print(list_folder_result)
    exit()

    while True:
        for sub_folder in list_folder_result.entries:
            handle_sub_folder(sub_folder)

        if not list_folder_result.has_more:
            break

        list_folder_result = dbx.files_list_folder_continue(list_folder_result.cursor)


def handle_sub_folder(subfolder):
    print(subfolder)

    # source = subfolder.path_lower
    # target_file = (
    #     "./"
    #     + TEMP_FOLDER
    #     + "/"
    #     + source.replace("/fotos/", "").replace("/", "--")
    #     + ".zip"
    # )

    # print("Start downloading folder: {0}".format(source))
    # dbx.files_download_zip_to_file(
    #     target_file,
    #     source,
    # )
    # print("Finished downloading folder: {0} into {1}".format(source, target_file))


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

check_temp_exists()
get_files_list(YEARS[0])
