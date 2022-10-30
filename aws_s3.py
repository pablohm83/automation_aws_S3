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

