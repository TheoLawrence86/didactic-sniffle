import boto3
import json
import os

# Path to save the keys
key_file = "ddap_keys.json"


def save_keys_to_file(access_key, secret_key):
    """
    Save the keys to a JSON file.
    """
    with open(key_file, "w") as f:
        json.dump({"AccessKeyId": access_key, "SecretAccessKey": secret_key}, f)
    print(f"New keys saved to {key_file}")


def create_new_access_key():
    """
    Create a new access key for the current IAM user.
    """
    try:
        iam = boto3.client('iam')

        # Create a new access key
        response = iam.create_access_key()
        access_key = response['AccessKey']['AccessKeyId']
        secret_key = response['AccessKey']['SecretAccessKey']

        print("New Access Key Created:")
        print(f"AccessKeyId: {access_key}")
        print(f"SecretAccessKey: {secret_key}")

        # Save the keys to a file
        save_keys_to_file(access_key, secret_key)

    except Exception as e:
        print(f"Error creating a new access key: {e}")
        exit(1)


if __name__ == "__main__":
    # Always create a new access key
    print("Creating a new access key...")
    create_new_access_key()
