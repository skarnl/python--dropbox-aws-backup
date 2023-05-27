# Dropbox to AWS Glacier

Script to download files from Dropbox, zip them and upload them to AWS.   
Mostly useful for backup purposes.

Some adjustment might be necessary, since the folder-structure is based on my personal Dropbox setup.

Adjust the `BASE_PHOTO_FOLDER_PATH` to make it reflect the path of your photos. And maybe adjust some logic with the `YEARS`.

Hope this script / repository can give some people more insight how to connect to Dropbox and/or upload files to AWS - I had to dig through a bunch of documentation and trial&error to get it all working.

#### Caveats
The script does work with multithreading ... but the progress-bar output will be kinda screwed 🤷

But it saves lots of time downloading and uploading all the files by yourself 😆

### Install

#### 1. Activate venv

Activate the Python virtual env 
```commandline
source venv/bin/activate
```

(to deactivate, just run )
```commandline
deactivate
```

#### 2. Install requirements
```commandline
pip3 install -r requirements.txt
```

### Dropbox access keys
You need the APP_KEY and APP_SECRET and set it in the `.env` (copy the `.env.example` and rename to `.env`)

You can find these values in your Dropbox account: https://www.dropbox.com/developers/apps

If you don't have an app here yet, create a new one, where the following permissions should be set:

- account_info.read
- files.metadata.read
- files.content.read