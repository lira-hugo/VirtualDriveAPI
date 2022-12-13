"""Programatically interact with a Google Cloud Storage bucket."""
import os
from os import listdir
from os.path import isfile, join
from os import environ
from random import randint
from google.cloud import storage
from GoogleCloud_Storage.config import bucketName, bucketFolder, localFolder
from GoogleCloud_Storage.authenticate_implicit_with_adc import authenticate_implicit_with_adc
import os
import pathlib
import mimetypes

# Autenticando o google cloud
authenticate_implicit_with_adc("global-incline-369522")
bucketName = 'turma_mtres2022_2_next'
storage_client = storage.Client()

bucket = storage_client.bucket(bucketName)

# Step 2. construct GCStorage instance
storage_client = storage.Client()
blobs = storage_client.list_blobs(bucketName)

def upload_files(bucket_name, filename):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    blob.upload_from_filename(filename)

    print(
        f"File {filename} uploaded to {blob}."
    )


def list_files(bucketName):
    """List all files in GCP bucket."""
    files = bucket.list_blobs(prefix=bucketFolder)
    fileList = [file.name for file in files if '.' in file.name]
    return fileList


def download_file(bucketName, bucketFolder):
    """Download random file from GCP bucket."""

    blob = bucket.blob(bucketFolder)
    fileName = blob.name.split('/')[-1]
    blob.download_to_filename(filename)
    return f'{fileName} downloaded from bucket.'


def list_files_with_prefix(bucket_name, prefix, delimiter=None):
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    # Note: The call returns a response only when the iterator is consumed.
    print("Blobs:")
    for blob in blobs:
        print(blob.name)

    if delimiter:
        print("Prefixes:")
        for prefix in blobs.prefixes:
            print(prefix)


def rename_file(bucket_name, blob_name, new_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    new_blob = bucket.rename_blob(blob, new_name)
    fileName = blob.name.split('/')[-1]
    print(f"Blob {fileName} has been renamed to {new_blob.name}")


def delete_file(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(blob_name)

    blob.delete()
    fileName = blob.name.split('/')[-1]

    print(f"Blob {fileName} deleted.")


