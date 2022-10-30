import logging
import boto3
from botocore.exceptions import ClientError
from botocore  import client
from botocore.client  import Config
import os

print('Ingresar Access key ID')
ACCESS_KEY_ID = input()
print('Ingresar Access secret key')
ACCESS_SECRET_KEY = input()

#Genero vars
#BUCKET_NAME='archivosutilitarios'
BUCKET_NAME='pruebatest3'
#FILE_NAME_DOWNLOAD='Dockerfile.txt'
FILE_NAME_DOWNLOAD='file_aws.txt'
#FILE_NAME_UPLOAD='/Users/pablocapelli/Desktop/projects/aws_s3/file_aws.txt'
PATH_DOWNLOAD='/Users/pablocapelli/Desktop/aws/file_aws.txt'
FILE_NAME_UPLOAD='/Users/pablocapelli/Desktop/projects/aws_s3/file_aws.txt'


#Genero conexión con aws

s3 = boto3.resource('s3',
    aws_access_key_id=ACCESS_KEY_ID, 
    aws_secret_access_key=ACCESS_SECRET_KEY)

#Generar bucket
def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
