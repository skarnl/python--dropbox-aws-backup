import boto3
from history import History
import os
import dotenv
import sys
import uuid
from tqdm import tqdm
from colorama import Fore
from utils.colorize import colorize

dotenv.load_dotenv()

s3_resource = boto3.client('s3')

aws_history = History("aws")

bucket_name = os.getenv("AWS_BUCKET_NAME")

if not bucket_name:
    print(colorize("No bucket_name found, provide one in the .env file", Fore.RED))
    sys.exit()

hist = aws_history.get_history()

def upload_zip(file_path, target_name):
    if target_name in hist:
        print(f"AWS upload : skip {colorize(target_name, Fore.BLUE)}, was uploaded earlier")
        return

    prefixed_target_name = ''.join([
        str(uuid.uuid4().hex[:6]),
        '__',
        target_name
    ])

    print(f"Upload to AWS: {colorize(prefixed_target_name, Fore.BLUE)}")

    file_size = os.stat(file_path).st_size

    with tqdm(total=file_size, unit="B", unit_scale=True, desc=file_path) as pbar:
        s3_resource.upload_file(
            file_path,
            bucket_name,
            prefixed_target_name,
            ExtraArgs={'ChecksumAlgorithm':'sha256'}
        )

    aws_history.add_to_history(target_name)