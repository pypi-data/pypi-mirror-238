import os
import boto3
import argparse


def s3_to_model(model_path, bucket_name, profile):
    # Checking if the model folder is empty
    if os.path.exists(model_path):
        folder_contents = os.listdir(model_path)
        if len(folder_contents) != 0:
            print("Local folder "+ model_path +" is not empty. Skipping")
            return True

    s3_prefix = os.path.basename(model_path)

    local_folder_path = model_path
    session = boto3.Session(profile_name=profile)
    s3 = session.client('s3')

    # List objects in the S3 bucket with the specified prefix
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)

    # Download each object to the local folder
    for obj in objects.get('Contents', []):
        s3_object_key = obj['Key']
        local_file_path = os.path.join(local_folder_path, os.path.relpath(s3_object_key, s3_prefix))

        # Create the local directory structure if it doesn't exist
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # Download the object from S3 to the local folder
        s3.download_file(bucket_name, s3_object_key, local_file_path)
        print(f'Downloaded s3://{bucket_name}/{s3_object_key} to {local_file_path}')


def model_to_s3(model_path, bucket_name, profile):
    local_folder_path = model_path
    base_name = os.path.basename(local_folder_path)
    session = boto3.Session(profile_name=profile)
    s3 = session.client('s3')

    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_folder_path)
            s3_object_key = os.path.join(base_name, relative_path)
            s3.upload_file(local_file_path, bucket_name, s3_object_key)
            print(f'Uploaded {local_file_path} to s3://{bucket_name}/{s3_object_key}')


def main():
    parser = argparse.ArgumentParser(description='Prepare and upload dataset to s3')
    parser.add_argument('--model', metavar='model', required=True,
                        help='the path to model')
    parser.add_argument('--bucket', metavar='bucket', required=True,
                        help='the bucket in s3')
    parser.add_argument('--profile', required=False,
                        help='aws profile to use for upload')
    parser.add_argument('--mode', choices=['upload', 'download', 'up', 'dl'])
    args = parser.parse_args()

    profile = os.environ.get("AWS_PROFILE")
    if args.profile is not None:
        profile = args.profile

    print("Using profile:" + profile + " to " + args.mode)

    if args.mode == "upload" or args.mode == "up":
        model_to_s3(args.model, args.bucket, profile)
    else:
        s3_to_model(args.model, args.bucket, profile)


if __name__ == '__main__':
    main()