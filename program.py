import logging
import json
from minio import Minio
from minio.error import S3Error

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("minio_access.log"),
            logging.StreamHandler()
        ]
    )

def load_minio_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            endpoint = config.get("endpoint")
            access_key = config.get("access_key")
            secret_key = config.get("secret_key")

            if not endpoint or not access_key or not secret_key:
                raise ValueError("Configuration file is missing required fields.")

            return endpoint, access_key, secret_key
    except Exception as e:
        logging.error(f"Failed to load MinIO configuration: {e}")
        raise

def connect_to_minio(endpoint, access_key, secret_key):
    try:
        client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )
        client.list_buckets()
        logging.info("Successfully connected to MinIO.")
        return client
    except S3Error as e:
        logging.error(f"MinIO connection failed: {e}")
        raise

def create_bucket(client, bucket_name):
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logging.info(f"Bucket '{bucket_name}' created successfully.")
        else:
            logging.info(f"Bucket '{bucket_name}' already exists.")
    except S3Error as e:
        logging.error(f"Error creating bucket '{bucket_name}': {e}")

# Use for deleting an empty bucket
def delete_bucket(client, bucket_name):
    try:
        if client.bucket_exists(bucket_name):
            client.remove_bucket(bucket_name)
            logging.info(f"Bucket '{bucket_name}' deleted successfully.")
        else:
            logging.info(f"Bucket '{bucket_name}' does not exist.")
    except S3Error as e:
        logging.error(f"Error deleting bucket '{bucket_name}': {e}")

# Use it to delete a bucket that is not empty
def force_delete_bucket(client, bucket_name):
    try:
        logging.info(f"Starting force deletion of bucket '{bucket_name}'...")

        objects = client.list_objects(bucket_name, recursive=True)
        for obj in objects:
            logging.info(f"Deleting object: {obj.object_name}")
            client.remove_object(bucket_name, obj.object_name)

        try:
            versioned_objects = client.list_objects(bucket_name, recursive=True, include_version=True)
            for versioned_obj in versioned_objects:
                logging.info(f"Deleting versioned object: {versioned_obj.object_name}, version_id: {versioned_obj.version_id}")
                client.remove_object(bucket_name, versioned_obj.object_name, version_id=versioned_obj.version_id)
        except S3Error as e:
            if e.code != "NoSuchBucket":  # Ignore if bucket does not exist after deleting all objects
                logging.warning(f"Error checking for versioned objects: {e}")

        logging.info(f"Deleting bucket: {bucket_name}")
        client.remove_bucket(bucket_name)
        logging.info(f"Bucket '{bucket_name}' and all its contents have been successfully deleted.")

    except S3Error as e:
        logging.error(f"Error deleting bucket '{bucket_name}': {e}")

def list_files(client, bucket_name):
    try:
        if client.bucket_exists(bucket_name):
            objects = client.list_objects(bucket_name)
            logging.info(f"Files in bucket '{bucket_name}':")
            for obj in objects:
                logging.info(f"- {obj.object_name}")
        else:
            logging.info(f"Bucket '{bucket_name}' does not exist.")
    except S3Error as e:
        logging.error(f"Error listing files in bucket '{bucket_name}': {e}")

def upload_file(client, bucket_name, file_path, object_name):

    try:
        client.fput_object(bucket_name, object_name, file_path)
        logging.info(f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
    except S3Error as e:
        logging.error(f"Error uploading file '{file_path}' to bucket '{bucket_name}': {e}")

def delete_object_from_bucket(client, bucket_name, object_name):
    try:
        client.remove_object(bucket_name, object_name)
        logging.info(f"Object '{object_name}' deleted from bucket '{bucket_name}'.")
    except S3Error as e:
        logging.error(f"Error deleting object '{object_name}' from bucket '{bucket_name}': {e}")

def get_bucket_policy(client, bucket_name):
    try:
        policy = client.get_bucket_policy(bucket_name)
        logging.info(f"Bucket policy for '{bucket_name}': {policy}")
        return policy
    except S3Error as e:
        logging.error(f"Error retrieving bucket policy for '{bucket_name}': {e}")

def set_bucket_policy(client, bucket_name, policy):
    try:
        client.set_bucket_policy(bucket_name, policy)
        logging.info(f"Bucket policy for '{bucket_name}' set successfully.")
    except S3Error as e:
        logging.error(f"Error setting bucket policy for '{bucket_name}': {e}")


def main():

    setup_logging()

    config_file = "minio_config.json"

    try:
        endpoint, access_key, secret_key = load_minio_config(config_file)

        client = connect_to_minio(endpoint, access_key, secret_key)

        bucket_name = "example-bucket"

        # create_bucket(client=client, bucket_name=bucket_name)
       
        # upload_file(client=client, bucket_name=bucket_name, file_path="example.txt", object_name="example.txt")
        
        # list_files(client=client, bucket_name=bucket_name)

        # policy = '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":"*","Action":"s3:GetObject","Resource":"arn:aws:s3:::example-bucket/*"}]}'
        # set_bucket_policy(client=client, bucket_name=bucket_name, policy=policy)
        
        # # If no policy is applied to the bucket, it will return an error message
        # get_bucket_policy(client=client, bucket_name=bucket_name)

        # delete_object_from_bucket(client=client, bucket_name=bucket_name, object_name="example.txt")
        
        # delete_bucket(client=client, bucket_name=bucket_name)
        # force_delete_bucket(client=client, bucket_name=bucket_name)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
