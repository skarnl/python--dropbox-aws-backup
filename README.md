# Dropbox to AWS Glacier

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