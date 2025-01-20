import boto3
import json
import os

# Path to save the keys
key_file = "ddap_keys.json"


def load_keys_from_file():
    """
    Load access keys from the JSON file.
    """
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            keys = json.load(f)
        return keys.get("AccessKeyId"), keys.get("SecretAccessKey")
    else:
        print(f"Key file {key_file} not found.")
        return None, None


def save_keys_to_file(access_key, secret_key):
    """
    Save the keys to a JSON file.
    """
    with open(key_file, "w") as f:
        json.dump({"AccessKeyId": access_key, "SecretAccessKey": secret_key}, f)
    print(f"New keys saved to {key_file}")


def check_access_key_validity(access_key, secret_key):
    """
    Check if the current access key is valid by using iam:ListAccessKeys.
    """
    try:
        iam = boto3.client(
            "iam",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        # Attempt to list the access keys for the current user
        response = iam.list_access_keys()
        if response['AccessKeyMetadata']:
            print("Access key is valid.")
            return True
        else:
            print("No valid access keys found.")
            return False
    except Exception as e:
        print(f"Access key is invalid or expired: {e}")
        return False


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
    # Load keys from the file
    access_key, secret_key = load_keys_from_file()

    # Check if the key is valid
    if access_key and secret_key and check_access_key_validity(access_key, secret_key):
        print("The current access key is valid. No new key is needed.")
    else:
        print("The current access key is invalid or missing. Creating a new key...")
        create_new_access_key()
