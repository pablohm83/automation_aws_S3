
import logging
from pickle import FALSE
import boto3
from botocore.exceptions import ClientError
import os
import json
import os.path


#Genero vars
ACCESS_KEY_ID=''
ACCESS_SECRET_KEY=''
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

menu_options = {
    1: 'Crear Bucket',
    2: 'Listar Buckets',
    3: 'Listar archivos en Bucket',
    4: 'Subir archivo',
    5: 'Bajar archivo',
    6: 'Obtener ACLs de un bucket',
    7: 'Exit',
}

def ask_user():
    OPTION_USER = input('Usar ACCESS KEYs de AWS CLI? [y/n]: ')
    if (OPTION_USER.lower() == 'n' or OPTION_USER.lower() == 'no'):
        global ACCESS_KEY_ID
        global ACCESS_SECRET_KEY
        ACCESS_KEY_ID = input('Ingresar Access key ID: ')
        ACCESS_SECRET_KEY = input('Ingresar Access secret key: ')
        try:
            #make instances client and resource with new credencials
            global s3
            global s3_client
            s3_client = boto3.client('s3',
                aws_access_key_id=ACCESS_KEY_ID,
                aws_secret_access_key=ACCESS_SECRET_KEY
                )

            s3 = boto3.resource('s3',
            aws_access_key_id=ACCESS_KEY_ID, 
            aws_secret_access_key=ACCESS_SECRET_KEY)
            
            #test credentials
            response = s3_client.list_buckets()
        except Exception as ex:
            print('Error en credenciales o conexion: '+str(ex))
            exit(1)            
        except:
            print('Error en credenciales o conexion')
            exit(1)
        return True
    elif (OPTION_USER.lower() == 'y' or OPTION_USER.lower() == 'yes'):
        try:
            response = s3_client.list_buckets()
        except Exception as ex:
            print('Error en credenciales o conexion: '+str(ex))
            exit(1)
        except:
            print('Error en credenciales o conexion')
            exit(1)        
        return True
    else:
        print('Opcion incorrecta, solo [y/n]')
        return False

def print_menu():
    print(' ')
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def get_acls(bucket_name):
    try:
        result = s3_client.get_bucket_acl(Bucket=bucket_name)
        json_formatted_str = json.dumps(result, indent=2)
        print(json_formatted_str)
    except Exception as ex:
        print('Error al obtener los ACL del bucket '+bucket_name+' Error: '+str(ex))
        return FALSE        
    except:
        print('Error al obtener los ACL del bucket: '+bucket_name)

def create_bucket(bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
    except Exception as ex:
        print("Error en creación de bucket: "+str(ex))
        return FALSE
    except:
        print("Error en creación de bucket ")
        return FALSE
    print ("Bucket "+BUCKET_NAME+" generado")
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
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    except Exception as ex:
        print('No se pudo subir el archivo pedido: '+str(ex))
        return False
    except:
        print('No se pudo subir el archivo pedido')
        return False
    print('Se subio el archivo '+file_name+' en el bucket '+bucket)
    return True

def download_file(path_download, file_name, bucket, object_name=None):
    try:
        pathandfile = os.path.join(path_download, file_name)
        s3.Bucket(bucket).download_file(file_name,pathandfile);
    except ClientError as e:
        print ('No se pudo bajar el file '+ str(e))
        return False
    except Exception as ex:
        print('No se pudo bajar el archivo pedido: '+str(ex))
        return False
    except:
        print ('No se pudo bajar el file pedido ')
        return False
    print ('Se bajo el File pedido: '+ file_name)
    return True

def list_buckets():
    try:
        response = s3_client.list_buckets()
    except ClientError as e:
        logging.error(e)
        print ('Error al listar Buckets: '+str(e))
        return False    
    print('Buckets existentes:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    print(' ')
    return True

def list_files_bucket(BUCKET_NAME):
    try:
        listBucket= s3.Bucket(BUCKET_NAME).objects.all()
        print ("Bucket: "+ s3.Bucket(BUCKET_NAME).name)
        print ("Files:")
        for item in listBucket:
            print ("    "+item.key)  
    except ClientError as e:
        print ('Error al listar archivos: '+str(e))
        return False
    except Exception as ex:
        print ('Error al listar archivos: '+str(ex))
        return False
    except:
        print ('Error al listar archivos:')
    return True
    
if __name__=='__main__':
    OK=False
    while (not OK):
        OK=ask_user()

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
            list_buckets()
            BUCKET_NAME = input('Ingrese el nombre del bucket para listar los archivos: ')
            list_files_bucket(BUCKET_NAME)
        elif option == 4:
            list_buckets()
            BUCKET_NAME = input('Ingrese el nombre del bucket donde se subira el achivo: ')
            FILE_NAME_UPLOAD = input('Ingrese el path y nombre del archivo. EJ: /home/file.txt: ')
            upload_file(FILE_NAME_UPLOAD,BUCKET_NAME)
        elif option == 5:
            list_buckets()
            BUCKET_NAME = input('Ingrese el nombre del bucket desde donde se bajara el achivo: ')
            out=list_files_bucket(BUCKET_NAME)
            if not out:
                continue
            FILE_NAME_DOWNLOAD = input('Ingrese el nombre del archivo a bajar: ')
            path_download=input('Ingrese el path destino: ')
            download_file(path_download, FILE_NAME_DOWNLOAD,BUCKET_NAME)
        elif option == 6:
            list_buckets()
            BUCKET_NAME = input('Ingrese el nombre del bucket para obtener las ACLs: ')
            get_acls(BUCKET_NAME)
        elif option == 7:
            exit()
        else:
            print('Opcion invalida. Ingresar un numero del 1 al 6.')
