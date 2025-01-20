import boto3
import os
import json

# AWS bucket and local directory information
bucket_name = "673310479191-e2cspearhead"
local_dir = "/home/localadmin/noctua/"
key_file = "ddap_keys.json"  # File containing the keys


def load_keys_from_file():
    """
    Load access keys from the JSON file.
    """
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            keys = json.load(f)
        return keys.get("AccessKeyId"), keys.get("SecretAccessKey")
    else:
        print(f"Key file {key_file} not found. Run the ddap_key_manager.py script first.")
        exit(1)


def download_dir(s3_client, prefix=''):
    """
    Download the contents of an S3 bucket to a local directory.
    """
    kwargs = {'Bucket': bucket_name}
    if prefix:
        kwargs['Prefix'] = prefix

    while True:
        resp = s3_client.list_objects_v2(**kwargs)
        for obj in resp.get('Contents', []):
            key = obj['Key']
            if not key.endswith('/'):  # Skip directories
                local_file_path = os.path.join(local_dir, key)
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                s3_client.download_file(bucket_name, key, local_file_path)
                print(f"Downloaded {key} to {local_file_path}")

        # Check if there are more objects to fetch
        if not resp.get('IsTruncated'):  # Stop if we've gotten all objects
            break

        # Set up for next iteration
        kwargs['ContinuationToken'] = resp.get('NextContinuationToken')


# Main script execution
if __name__ == "__main__":
    # Load AWS credentials from the JSON file
    access_key, secret_key = load_keys_from_file()

    # Create an S3 client with the loaded credentials
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    # Start downloading files from the S3 bucket
    print("Starting download...")
    download_dir(s3)
    print("Download completed.")
