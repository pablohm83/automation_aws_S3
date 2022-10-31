import logging
import boto3
from botocore.exceptions import ClientError
from botocore  import client
from botocore.client  import Config
import os

ACCESS_KEY_ID = input('Ingresar Access key ID')
ACCESS_SECRET_KEY = input('Ingresar Access secret key')


#Genero vars
menu_options = {
    1: 'Crear Bucket',
    2: 'Listar Buckets',
    3: 'Listar archivos en Bucket',
    4: 'Subir archivo',
    5: 'Bajar archivo',
    6: 'Obtener ACLs de un bucket',
    7: 'Exit',
}


def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def get_acls(bucket_name):
    try:
        result = s3_client.get_bucket_acl(Bucket=bucket_name)
        print(result)
    except:
        print('Error al obtener la data ')

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
    print ("Bucket "+BUCKET_NAME+" generado")
    return True

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    #COMPRESS FILES tar.gz 

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        s3_client = boto3.client('s3',
            aws_access_key_id=ACCESS_KEY_ID, 
            aws_secret_access_key=ACCESS_SECRET_KEY)
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    print('Se subio el archivo '+file_name+' en el bucket '+bucket)
    return True

def download_file(path_download, file_name, bucket, object_name=None):
    try:
        s3.Bucket(bucket).download_file(file_name,path_download+'/'+file_name);
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print('No existe el file')
            return False
        else:
            raise
    return True
    print ('Se bajo el File pedido: '+ file_name)

def list_buckets():
    try:
        s3_client = boto3.client('s3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY
            )
    except ClientError as e:
        logging.error(e)
        return False    
    response = s3_client.list_buckets()
        # Output the bucket names
    print('Buckets existentes:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    return True

def list_files_bucket(BUCKET_NAME):
    try:
        listBucket= s3.Bucket(BUCKET_NAME).objects.all()
    except ClientError as e:
        logging.error(e)
        return False    
    print ("Bucket: "+ s3.Bucket(BUCKET_NAME).name)
    print ("Files:")
    for item in listBucket:
        print ("    "+item.key)
    return True

if __name__=='__main__':
    #chequeo de credenciales OK
    try:
        s3_client = boto3.client('s3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY
            )
        s3_client.list_buckets()
    except:
        print('Error en credenciales')
        exit(1)

    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Ingresá la acción a ejecutar: '))
        except:
            print('Error, Solo ingreso numerico ...')
        if option == 1:
            BUCKET_NAME = input('Ingrese el nombre del bucket a crear: ')
            create_bucket(BUCKET_NAME)
        elif option == 2:
            list_buckets()
        elif option == 3:
            BUCKET_NAME = input('Ingrese el nombre del bucket para listar los archivos: ')
            list_files_bucket(BUCKET_NAME)
        elif option == 4:
            BUCKET_NAME = input('Ingrese el nombre del bucket donde se subira el achivo: ')
            FILE_NAME_UPLOAD = input('Ingrese el path y nombre del archivo. EJ: /home/file.txt: ')
            upload_file(FILE_NAME_UPLOAD,BUCKET_NAME)
        elif option == 5:
            BUCKET_NAME = input('Ingrese el nombre del bucket desde donde se bajara el achivo: ')
            FILE_NAME_DOWNLOAD = input('Ingrese el nombre del archivo a bajar: ')
            path_download=input('Ingrese el path destino: ')
            download_file(path_download, FILE_NAME_DOWNLOAD,BUCKET_NAME)
        elif option == 6:
            BUCKET_NAME = input('Ingrese el nombre del bucket para obtener las ACLs ')
            get_acls(BUCKET_NAME)
        elif option == 7:
            exit()
        else:
            print('Opcion invalida. Ingresar un numero del 1 al 6.')
