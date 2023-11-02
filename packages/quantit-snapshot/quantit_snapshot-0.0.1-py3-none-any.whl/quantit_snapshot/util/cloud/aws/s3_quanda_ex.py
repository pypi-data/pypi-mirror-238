import os
import boto3

from quantit_snapshot.util.config.log.log import get_logger

LOGGER = get_logger()


class S3QuandaEx:
    @staticmethod
    def upload_file(file_name, object_name, bucket, aws_key, aws_secret_key):
        s3_client = boto3.client('s3', aws_access_key_id=aws_key,
                                 aws_secret_access_key=aws_secret_key)
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            return False
        return True

    @staticmethod
    def download_file(file_name, object_name, bucket, aws_key, aws_secret_key):
        try:
            with open(file_name, 'wb') as f:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=aws_secret_key
                )
                s3_client.download_fileobj(bucket, object_name, f)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            return False
        return True

    @staticmethod
    def delete_file(object_name, bucket, aws_key, aws_secret_key):
        try:
            s3_client = boto3.client('s3', aws_access_key_id=aws_key,
                                     aws_secret_access_key=aws_secret_key)
            s3_client.delete_object(Bucket=bucket, Key=object_name)
        except s3_client.exceptions.NoSuchKey:
            LOGGER.info(f'no such key in bucket bucket:{bucket} object_name: {object_name}')
            return False
        return True

    @staticmethod
    def put_data(data, object_name, bucket, aws_key, aws_secret_key):
        s3_client = boto3.client('s3', aws_access_key_id=aws_key,
                                 aws_secret_access_key=aws_secret_key)
        s3_client.put_object(Body=data, Bucket=bucket, Key=object_name)

    @staticmethod
    def get_data(object_name, bucket, aws_key, aws_secret_key):
        try:
            s3_client = boto3.client('s3', aws_access_key_id=aws_key,
                                     aws_secret_access_key=aws_secret_key)
            response = s3_client.get_object(Bucket=bucket, Key=object_name)
            return response['Body'].read()
        except s3_client.exceptions.NoSuchKey:
            LOGGER.info(f'no such key in bucket bucket:{bucket} object_name: {object_name}')
            return None

    @staticmethod
    def get_size(object_name, bucket, aws_key, aws_secret_key):
        try:
            s3_client = boto3.client('s3', aws_access_key_id=aws_key,
                                     aws_secret_access_key=aws_secret_key)
            response = s3_client.head_object(Bucket=bucket, Key=object_name)
            return response['ContentLength']
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            return 0

    @staticmethod
    def get_obj_list(prefix, bucket, aws_key, aws_secret_key):
        try:
            s3_client = boto3.client('s3', aws_access_key_id=aws_key,
                                     aws_secret_access_key=aws_secret_key)
            paginator = s3_client.get_paginator('list_objects_v2')
            response_iterator = paginator.paginate(
                Bucket=bucket,
                Prefix=prefix
            )
            result = []
            for page in response_iterator:
                for content in page['Contents']:
                    result.append(content['Key'])
            return result
        except:
            return None

    @staticmethod
    def download_folder(
            obj_folder,
            local_folder,
            bucket,
            aws_key,
            aws_secret_key,
    ):
        def _is_path(filename):
            if filename.endswith(os.path.sep):
                return True
            else:
                return False

        try:
            files = S3QuandaEx.get_obj_list(obj_folder, bucket, aws_key, aws_secret_key)
            os.makedirs(local_folder, exist_ok=True)
            for obj in files:
                if _is_path(obj):
                    continue
                local_dir = os.path.join(
                    local_folder,
                    os.path.basename(obj)
                )
                S3QuandaEx.download_file(
                    local_dir, obj, bucket, aws_key, aws_secret_key
                )
        except:
            return
