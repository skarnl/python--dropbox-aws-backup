import os
import sys

import dropbox
import http
import concurrent.futures

from utils import db_download, db_auth, aws_upload
from utils.colorize import colorize
import shutil
from history import History

from colorama import init, Fore

init(autoreset=True)

db_history = History("dropbox")

# ENABLE THIS WHEN DEVELOPING, TO ONLY DOWNLOAD A SMALL AMOUNT OF FILES
DEVELOPMENT_MODE=False

BASE_PHOTO_FOLDER_PATH = "/fotos"
TEMP_FOLDER = "./__temp_folder__"

MAX_MONTHS_TO_PROCESS = 10

months_processed_count = 0

processing = True

refresh_retries = 0

YEARS = [
    # "2007-en-ervoor",
    # "2008",
    # "2009",
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022"
]

dbx = db_auth.get_dropbox_client()

if not dbx:
    print(colorize("No dropbox client to work with", Fore.RED))
    exit()


def reset_temp_dir():
    print(f"{Fore.YELLOW}Clearing all files from temp directory: {TEMP_FOLDER}")

    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)

    os.makedirs(TEMP_FOLDER)


# get all folders and files from the given year
def get_files_list(year):
    global months_processed_count
    global refresh_retries

    print(f"Start processing {colorize(year, Fore.BLUE)}")

    hist = db_history.get_history()

    if year in hist:
        print(f"Skip {colorize(year, Fore.BLUE)} since thats already handled fully")
        return

    folder_list = []

    list_folder_result = dbx.files_list_folder(path=BASE_PHOTO_FOLDER_PATH + "/" + year)

    refresh_retries = 0

    def process_entries(entries):
        for sub_folder in entries:
            if isinstance(sub_folder, dropbox.files.FolderMetadata):
                folder_list.append(sub_folder.path_lower)

    process_entries(list_folder_result.entries)

    while list_folder_result.has_more:
        list_folder_result = dbx.files_list_folder_continue(list_folder_result.cursor)

        process_entries(list_folder_result.entries)


    if DEVELOPMENT_MODE:
        print(colorize(f"RUNNING IN DEVELOPMENT_MODE, SO ONLY 3 SUBFOLDERS ARE PROCESSED", Fore.GREEN))

        folder_list = folder_list[:5]


    for sf in folder_list:
        key = year + sf

        if key not in hist:
            handle_sub_folder(sf)

            print(f"Month {colorize(sf, Fore.BLUE)} done, up to next month\n")
            db_history.add_to_history(key)

            months_processed_count += 1

            if months_processed_count >= MAX_MONTHS_TO_PROCESS:
                print(colorize(f"Max number of months reached - breaking for now. Last month progressed = {key}"), Fore.CYAN)
                sys.exit()
        else:
            print(f"{colorize(key, Fore.BLUE)} skipped")

    # close full year
    db_history.add_to_history(year)
    print(f"Year {colorize(year, Fore.BLUE)} closed, proceed with next year\n")


# download all files from this month
# archive them into a zip-file
# and upload to AWS
def handle_sub_folder(subfolder):
    clean_subfolder_name = subfolder.replace("/fotos/", "").replace("/", "--")

    target_dir = os.path.join(
        TEMP_FOLDER,
        clean_subfolder_name + "/",
    )

    # create the target dir
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # download all photos into the target-dir
    db_download.get_files(dbx, subfolder, target_dir, DEVELOPMENT_MODE)

    # zip the target_dir
    zip_file_path = os.path.join(TEMP_FOLDER, clean_subfolder_name)

    if not os.path.exists(zip_file_path + '.zip'):
        print(f"Create {clean_subfolder_name}.zip")

        shutil.make_archive(
            base_name=zip_file_path,
            format='zip',
            root_dir=TEMP_FOLDER,
            base_dir=clean_subfolder_name,
        )

    # upload the zip to aws (with checksum!)
    aws_upload.upload_zip(os.path.join(TEMP_FOLDER, clean_subfolder_name) + '.zip', f"{clean_subfolder_name}.zip")

    # cleanup: remove the zip and target_dir


if __name__ == "__main__":

    # uncomment to reset every local progress
    # reset_temp_dir()
    # db_history.reset()

    while processing:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                executor.map(get_files_list, YEARS)

            hist = db_history.get_history()
            if all(x in hist for x in YEARS):
                print(colorize("We are finished. All years are done.", Fore.GREEN))
                processing = False
                break

        except (dropbox.exceptions.AuthError, http.client.RemoteDisconnected) as e:
            print(colorize("dropbox.exceptions.AuthError", Fore.RED))
            print(e)

            if refresh_retries > 5:
                print("We retried multiple times - lets bail")
                processing = False
                break

            dbx = db_auth.refresh_client()
            refresh_retries += 1


