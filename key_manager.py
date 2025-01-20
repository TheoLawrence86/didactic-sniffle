import boto3
import json
import os

# Load keys from the saved file
key_file = "ddap_keys.json"


def load_keys_from_file():
    """
    Load keys from the JSON file.
    """
    if not os.path.exists(key_file):
        print(f"Key file {key_file} not found. Please run ddap_key_manager.py to generate keys.")
        exit(1)

    with open(key_file, "r") as f:
        keys = json.load(f)

    return keys["AccessKeyId"], keys["SecretAccessKey"]


def download_s3_objects(bucket_name, prefix='', local_dir='.'):
    """
    Download objects from S3.
    """
    access_key, secret_key = load_keys_from_file()

    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    kwargs = {'Bucket': bucket_name}
    if prefix:
        kwargs['Prefix'] = prefix

    resp = s3.list_objects_v2(**kwargs)
    for obj in resp.get('Contents', []):
        key = obj['Key']
        local_file_path = os.path.join(local_dir, key)
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        s3.download_file(bucket_name, key, local_file_path)
        print(f"Downloaded {key} to {local_file_path}")


if __name__ == "__main__":
    # Example usage
    download_s3_objects(bucket_name="673310479191-e2cspearhead", local_dir="/home/localadmin/noctua")
