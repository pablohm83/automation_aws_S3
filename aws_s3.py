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
