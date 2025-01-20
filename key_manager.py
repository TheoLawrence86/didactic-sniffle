import boto3
import os
import json

# Path to save the AWS keys
key_file = "ddap_keys.json"


def save_keys_to_file(access_key, secret_key):
    """
    Save the keys to a JSON file.
    """
    with open(key_file, "w") as f:
        json.dump({"AccessKeyId": access_key, "SecretAccessKey": secret_key}, f)
    print(f"Keys saved to {key_file}")


def load_keys_from_file():
    """
    Load keys from the JSON file.
    """
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            keys = json.load(f)
        return keys.get("AccessKeyId"), keys.get("SecretAccessKey")
    return None, None


def check_access_key_validity(access_key, secret_key):
    """
    Check if the current access key is valid by listing buckets.
    """
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        s3.list_buckets()  # Attempt to list buckets
        print("Access key is valid.")
        return True
    except Exception as e:
        print("Access key is invalid or expired:", e)
        return False


def get_new_access_key():
    """
    Create a new access key.
    """
    iam = boto3.client('iam')
    try:
        response = iam.create_access_key()
        new_access_key = response['AccessKey']['AccessKeyId']
        new_secret_key = response['AccessKey']['SecretAccessKey']

        print("New Access Key ID:", new_access_key)
        print("New Secret Access Key:", new_secret_key)

        return new_access_key, new_secret_key
    except Exception as e:
        print("Error creating a new access key:", e)
        return None, None


# Main logic
if __name__ == "__main__":
    # Load keys from the JSON file or assume no valid key exists
    access_key, secret_key = load_keys_from_file()

    # Validate the keys
    if not access_key or not secret_key or not check_access_key_validity(access_key, secret_key):
        # Create a new access key if the existing one is invalid or missing
        access_key, secret_key = get_new_access_key()
        if access_key and secret_key:
            save_keys_to_file(access_key, secret_key)
        else:
            print("Failed to create a new access key. Exiting.")
            exit(1)
