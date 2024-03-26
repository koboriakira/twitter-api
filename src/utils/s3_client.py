import contextlib
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


class S3Client:
    """ファイルをS3上で読み書きする"""

    BUCKET_NAME = "twitter-api-bucket-koboriakira"

    def __init__(self) -> None:
        self.s3_client = boto3.client("s3")

    def upload(self, file_path: str) -> None:
        """ファイルをS3にアップロード"""
        self.s3_client.upload_file(file_path, self.BUCKET_NAME, file_path)

    def download(self, file_path: str) -> None:
        """S3からファイルをダウンロード"""
        if Path(file_path).exists():
            return  # すでにファイルが存在する場合は何もしない

        with contextlib.suppress(ClientError):
            self.s3_client.download_file(self.BUCKET_NAME, file_path, file_path)
