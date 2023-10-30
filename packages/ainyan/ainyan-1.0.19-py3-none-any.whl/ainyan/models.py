# from ainyan.zippers import *
import os
import boto3
from ainyan import zip_folder, unzip_folder

def model_to_s3(model_path, s3_bucket_name):
    basename = os.path.basename(model_path)

    zip_filename = basename + ".zip"

    zip_folder(model_path, zip_filename)

    # Upload the zipped file to S3
    # s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3 = boto3.client('s3')
    s3.upload_file(zip_filename, s3_bucket_name, zip_filename)
    # TODO: for later
    # os.remove(zip_filename)


def model_from_s3(s3_path):
    s3 = boto3.client('s3')

    s3_bucket = os.path.dirname(s3_path)
    zip_file = os.path.basename(s3_path)

    # Download the zip file from S3
    s3.download_file(s3_bucket, zip_file, zip_file)
    local_path = os.path.splitext(zip_file)[0]
    unzip_folder(zip_file, local_path)

    # Clean up the downloaded zip file
    os.remove(zip_file)