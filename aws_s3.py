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
BUCKET_NAME='archivosutilitarios'
#BUCKET_NAME='pruebatest3'
#FILE_NAME_DOWNLOAD='Dockerfile.txt'
FILE_NAME_DOWNLOAD='file_aws.txt'
#FILE_NAME_UPLOAD='/Users/pablocapelli/Desktop/projects/aws_s3/file_aws.txt'
PATH_DOWNLOAD='/Users/pablocapelli/Desktop/aws/file_aws.txt'
FILE_NAME_UPLOAD='/Users/pablocapelli/Desktop/projects/aws_s3/file_aws.txt'


#Genero conexión con aws resource y client
s3 = boto3.resource('s3',
    aws_access_key_id=ACCESS_KEY_ID, 
    aws_secret_access_key=ACCESS_SECRET_KEY)

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
            s3_client = boto3.client('s3',
                aws_access_key_id=ACCESS_KEY_ID, 
                aws_secret_access_key=ACCESS_SECRET_KEY)
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region,
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY)
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

def download_file(file_name, bucket, object_name=None):
    try:
        s3.Bucket(bucket).download_file(file_name,PATH_DOWNLOAD);
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print('No existe el file')
            return False
        else:
            raise
    print ('Se bajo el File pedido: '+ file_name)

def list_buckets():
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
        # Output the bucket names
    print('Buckets existentes:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

def list_files_bucket(BUCKET_NAME):
    listBucket= s3.Bucket(BUCKET_NAME).objects.all()
    print ("Bucket: "+ s3.Bucket(BUCKET_NAME).name)
    print ("Files:")
    for item in listBucket:
        print ("    "+item.key)

create_bucket('archivos-a-analizar')
#upload_file(FILE_NAME_UPLOAD, BUCKET_NAME)
#lista_buckets()
#list_files_bucket('archivos-a-analizar')
#download_file(FILE_NAME_DOWNLOAD,BUCKET_NAME)
