# README
Challenge MeLi AWS S3

<br>

## Sipnosis

El siguiente script se utliza para interactuar con el servicio de Buckets de AWS. Desde el mismo es posible realizar:
<br>
* Creación de Buckets
* Listado de Buckets del usuario
* Listado de archivos sobre un determinado Bucket
* Subida de archivos desde una máquina de usuario o EC2 a un Bucket
* Bajada de archivos desde un Bucket a una máquina de usuario o EC2
* Obtención de ACLs de un bucket pedido

Es multiplataforma (funciona en Windows, MacOs y Linux, entre otros)

## Variables adicionales y/o parámetros

No requeridos.

<br>

## Resultados de ejecución

Código de retorno(RCN) |  Descripción
----------|---------
0 | El script finalizó correctamente.
1 | Error de credenciales o conexión, el script finaliza inmediatamente.
<br>

**Los errores de ejecución luego de verificación de credenciales se mostrarán en pantalla.**

<br>

## Soporte

En caso de necesitar reportar errores, por favor hacerlo mediante Issues de este repositorio o por mail a: 

<pablocapelli@gmail.com>

<br>

## Problemas conocidos y limitaciones

**No es posible subir o bajar multiples archivos a la vez.**

<br>

## Pre-requisitos

* Python 2.7+ o Python 3.4+
* Tener instalado el SDK Boto3 para Python
    * Python 2.7+ --> pip install boto3
    * Python 3.4+ --> pip3 install boto3
* Ejecutar el script con permisos mínimos de Escritura en el directorio de bajada y permisos de lectura en el directorio de subida


<br>

## Ejemplo de ejecución para listar Buckets

```	python3 aws_s3_0.2.py
	Usar ACCESS KEYs de AWS CLI? [y/n]: y			--> Consulta de credenciales
	
	**MENU**
	
	1 -- Crear Bucket
	2 -- Listar Buckets
	3 -- Listar archivos en Bucket
	4 -- Subir archivo
	5 -- Bajar archivo
	6 -- Obtener ACLs de un bucket
	7 -- Exit
	Ingresá la acción a ejecutar: 2				--> Opción 2: "Listar Buckets"
	
	Buckets existentes:					--> Output
	  archivos-a-analizar
	  archivos-utilitarios
```

<br>


