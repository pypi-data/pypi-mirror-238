#!/usr/bin/env python3

"""
A program to download all the AWS cloudfront log files for a
service on a day and create a single merged log file.
"""

import boto3
import click
import configparser
from datetime import datetime, timedelta
import os
import subprocess
from typing import List, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import sys


def list_matching_files(s3: Any, bucket_name: str, prefix: str) -> List[str]:
    """
    List files in an S3 bucket that match a given prefix.

    This function uses paginated results to retrieve all matching files, making it
    suitable for buckets with a large number of files.

    :param s3: Boto3 S3 client object.
    :type s3: Any
    :param bucket_name: Name of the S3 bucket to search within.
    :type bucket_name: str
    :param prefix: The prefix string to match files against.
    :type prefix: str
    :return: A list of matching file keys (S3 object keys).
    :rtype: List[str]
    """
    # Initialize a list to store matching filenames
    matching_files = []

    # Paginator helps in case there are many files and results span multiple pages
    paginator = s3.get_paginator("list_objects_v2")

    # Iterate over each page of results
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        # Check if 'Contents' key exists (it might not if no results are returned)
        if "Contents" in page:
            for obj in page["Contents"]:
                matching_files.append(obj["Key"])

    return matching_files


def download_file(s3: Any, bucket: str, file_key: str, download_dir: str) -> None:
    """
    Download a file from an S3 bucket.

    This function checks whether the file is already present locally with the
    same size as in the S3 bucket. If the file does not exist locally or has a
    different size, it will be downloaded.

    :param s3: Boto3 S3 client object.
    :type s3: Any
    :param bucket: Name of the S3 bucket from where the file will be downloaded.
    :type bucket: str
    :param file_key: S3 object key of the file to be downloaded.
    :type file_key: str
    :param download_dir: The local directory where the downloaded file will be stored.
    :type download_dir: str
    :return: None
    """
    local_path = os.path.join(download_dir, os.path.basename(file_key))
    s3_head = s3.head_object(Bucket=bucket, Key=file_key)
    s3_file_size = s3_head["ContentLength"]

    if not os.path.exists(local_path) or os.path.getsize(local_path) != s3_file_size:
        #print(f"Downloading {file_key}...")
        s3.download_file(bucket, file_key, local_path)


def parallel_download_files(
    s3: Any, bucket_name: str, files: List[str], download_dir: str, max_workers: int
) -> None:
    """
    Downloads files from an S3 bucket in parallel.

    This function uses a thread pool to download files concurrently from an S3 bucket.
    The S3 client is passed as an argument.

    :param s3: Boto3 S3 client object.
    :type s3: Any
    :param bucket_name: Name of the S3 bucket from where files will be downloaded.
    :type bucket_name: str
    :param files: A list of S3 object keys that need to be downloaded.
    :type files: List[str]
    :param download_dir: The local directory where the downloaded files will be stored.
    :type download_dir: str
    :param max_workers: Maximum number of worker threads.
    :type max_workers: int
    :return: None
    """
    # Ensure the download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(download_file, s3, bucket_name, file_key, download_dir)
            for file_key in files
        ]

        for future in futures:
            future.result()  # This line can be used to handle exceptions or get results returned from the function

    #print("Download completed.")


@click.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--date",
    default=None,
    help="Specific date for which the logs are to be fetched, in the format YYYY-MM-DD. If not provided, it defaults to the previous day's date.",
)
def main(config_file: str, date: Optional[str]) -> None:
    """
    Download AWS Cloudfront logs from an S3 bucket for a specific date.

    This script downloads logs from an AWS S3 bucket for a given date (or for the previous day if no date is provided).
    The logs are filtered to include only the entries for the specified date and are then written to a gzipped file.

    Usage:
        merges3logs path/to/CONFIG_FILE --date YYYY-MM-DD
    """

    # Load Configuration
    cfg = configparser.ConfigParser()
    cfg.read(config_file)
    aws_access_key = cfg.get("AWS", "AccessKey")
    aws_secret_key = cfg.get("AWS", "SecretKey")
    bucket_name = cfg.get("S3", "BucketName")
    bucket_prefix = cfg.get("S3", "Prefix")
    max_workers = int(cfg.get("S3", "MaxWorkers", fallback=5))
    cache_dir = cfg.get("Local", "CacheDir")
    dest_dir = cfg.get("Local", "DestDir")
    dest_filename = cfg.get("Local", "DestFilename")
    remove_files = bool(cfg.get("Local", "RemoveFiles", fallback="True"))

    # Setup S3 client
    s3 = boto3.client(
        "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
    )

    # Date Handling
    if not date:
        target_date = datetime.utcnow() - timedelta(days=1)
    else:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    next_day = target_date + timedelta(days=1)

    # Downloading
    files_to_download = list_matching_files(
        s3, bucket_name, target_date.strftime(bucket_prefix)
    )
    files_to_delete = files_to_download.copy() if remove_files else []
    files_to_download.extend(
        list_matching_files(s3, bucket_name, next_day.strftime(bucket_prefix))
    )
    parallel_download_files(s3, bucket_name, files_to_download, cache_dir, max_workers)

    # Process and Write to Pipeline
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    sort_proc = subprocess.Popen(
        f"sort -k3 | gzip >{os.path.join(dest_dir, target_date.strftime(dest_filename))}.gz",
        stdin=subprocess.PIPE,
        shell=True,
        text=True,
    )

    date_prefix = f'[{target_date.strftime("%d/%b/%Y")}:'
    for file in [os.path.basename(x) for x in files_to_download]:
        with open(os.path.join(cache_dir, file), "r") as f:
            for line in f:
                fields = line.split()
                if len(fields) > 2 and fields[2].startswith(date_prefix):
                    sort_proc.stdin.write(line)
    sort_proc.stdin.close()
    retcode = sort_proc.wait()

    if retcode != 0:
        print(f"ERROR: sort/compress exited {retcode} != 0")

    if remove_files:
        for file in files_to_delete:
            os.remove(os.path.join(cache_dir, os.path.basename(file)))

    sys.exit(retcode)


if __name__ == "__main__":
    main()
