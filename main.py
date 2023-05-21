import os
from utils import db_download, db_auth
import shutil
import history

BASE_PHOTO_FOLDER_PATH = "/fotos"
TEMP_FOLDER = "./__temp_folder__"

YEARS = [
    # "2007-en-ervoor",
    "2008",
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

dbx = db_auth.get_dropbox_client()

if not dbx:
    print("No dropbox client to work with")
    exit()


def reset_temp_dir():
    print(f"Clearing all files from temp directory: {TEMP_FOLDER}")

    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)

    os.makedirs(TEMP_FOLDER)


# get all folders and files from the given year
def get_files_list(year):
    print(f"Start processing {year}")

    hist = history.get_history()

    if year in hist:
        print(f"Skip {year} since thats already handles fully")
        return

    folder_list = []

    list_folder_result = dbx.files_list_folder(path=BASE_PHOTO_FOLDER_PATH + "/" + year)

    def process_entries(entries):
        for sub_folder in entries:
            folder_list.append(sub_folder.path_lower)

    process_entries(list_folder_result.entries)

    while list_folder_result.has_more:
        list_folder_result = dbx.files_list_folder_continue(list_folder_result.cursor)

        process_entries(list_folder_result.entries)


    # TODO: REMOVE THIS, ALSO IN db_download WE DO LESS FILES DOWNLOAD
    folder_list = folder_list[:3]


    for sf in folder_list:
        key = year + sf

        if key not in hist:
            handle_sub_folder(sf)

            print(f"Month {sf} done, up to next month")
            history.add_to_history(key)
        else:
            print(f"{key} skipped")

    # close full year
    history.add_to_history(year)
    print(f"Year {year} closed, proceed with next year")


def handle_sub_folder(subfolder):
    target_dir = os.path.join(
        TEMP_FOLDER,
        subfolder.replace("/fotos/", "").replace("/", "--") + "/",
    )

    # create the target dir
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # download all photos into the target-dir
    db_download.get_files(dbx, subfolder, target_dir)

    # zip the target_dir


    # upload the zip to aws (with checksum!)

    # cleanup: remove the zip and target_dir


if __name__ == "__main__":

    # uncomment to reset every local progress
    # reset_temp_dir()
    history.reset()

    for current_year in YEARS:
        get_files_list(current_year)
