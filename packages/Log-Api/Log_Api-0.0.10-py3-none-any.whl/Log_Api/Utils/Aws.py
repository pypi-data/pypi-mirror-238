import logging
import os
import json
import boto3
import base64
import json
from botocore.exceptions import NoCredentialsError, ClientError
from Utils.Exceptions import UserException


class Aws:

    @classmethod
    def get_secret(cls, name='secret-fcc'):
        """
        Obtener secreto
        param: str
            name llave del nombre del secreto a obtener
        """
        stage = os.getenv('STAGE')

        secretname = f'{stage}/{name}'

        client = cls.get_client('secretsmanager')

        try:
            secret_request = client.get_secret_value(
                SecretId=secretname
            )
        except client.exceptions.ResourceNotFoundException as e:
            raise ValueError(f"No se encontró el secreto {e}")
        except client.exceptions.InvalidParameterException as e:
            raise ValueError(f"InvalidParameterException {e}")
        except client.exceptions.InvalidRequestException as e:
            raise ValueError(f"InvalidRequestException {e}")
        except client.exceptions.DecryptionFailure as e:
            raise ValueError(f"DecryptionFailure {e}")
        except client.exceptions.InternalServiceError as e:
            raise ValueError(f"InternalServiceError {e}")
        except Exception as e:
            raise ValueError(f"Error en el secreto {e}")

        if 'SecretString' in secret_request:
            secret = secret_request['SecretString']
        else:
            secret = base64.b64decode(secret_request['SecretBinary'])

        return json.loads(secret)

    @classmethod
    def function_name(cls, function: str, service: str, stage=os.getenv('STAGE'), app=os.getenv('APP')):
        """
        Crea nombre de función lambda
        :param: function
            nombre de la función
        :param: stage
            nombre del stage
        :param: app
            nombre de la aplicación
        :return: function_name
        """
        return f"{app}-{service}-{stage}-{function}"
    
    @classmethod
    def get_client(cls, service_name: str):
        """
        Obtener cliente de aws
        param: service_name
            nombre del servicio
        return: client
            cliente de aws
        """
        session = boto3.session.Session()
        client = session.client(
            service_name=service_name,
            region_name=os.getenv('REGION')
        )
        return client

    @classmethod
    def lambdaInvoke(cls, function_name: str, data: dict = {}, inv_type: str = 'RequestResponse') -> dict:
        """
            Invocar lambda
        Args:
            function_name (str): Nombre de la función lambda
            data (dict): Datos a enviar a la función lambda
            inv_type (str): Tipo de invocación de la función lambda
        
        Returns:
            response (dict): Respuesta de la función lambda
        """
        if inv_type == 'RequestResponse':
            data = {'body': json.dumps(data)}
        
        data = json.dumps(data)
        
        client = cls.get_client('lambda')
        response = client.invoke(
            FunctionName=function_name,
            Payload=data,
            LogType='Tail',
            InvocationType=inv_type
        )
        
        if inv_type == 'RequestResponse':
            response_document = response['Payload'].read().decode(
                'utf-8')
            response_document = json.loads(response_document)
            print('response_document', response_document)
            response = json.loads(response_document.get('body', '{}'))

        return response

    @classmethod
    def put_in_s3(cls, array_byte, file_path: str):
        """
        Subir archivo a S3
        :param: file_name
            nombre del archivo, debe tener esta estructura:
                carpeta/nombre_archivo.extension
        :param: file_path
            ruta del archivo a subir
        :return: s3_path_file
        """

        # Get S3 info
        secrets = Aws.get_secret("s3-fcc")

        # S3 Bucket Name
        bucket_name = secrets["bucket_name"]

        s3 = boto3.client('s3') 
        try:
            if type(array_byte) == bytes:
                response = s3.put_object(Body=array_byte, Bucket= bucket_name,
                            Key= file_path)
                if response.get('ResponseMetadata').get('HTTPStatusCode') != 200:
                    raise UserException("Error al guardar el archivo")
            else:
                response = s3.upload_file(file_path, bucket_name, array_byte)
        except NoCredentialsError:
            raise NoCredentialsError("Credenciales invalidas")
        except Exception as e:
            raise e

    @classmethod
    def delete_s3_file(cls, file_path: str):
        """
        Eliminar archivo de S3
        :param: file_path
            ruta del archivo, debe tener esta estructura:
                carpeta/nombre_archivo.extension
        """
        # Get S3 info
        secrets = Aws.get_secret("s3-fcc")

        # S3 Bucket Name
        bucket_name = secrets["bucket_name"]

        # Put object to bucket
        s3_client = boto3.client('s3')

        try:
            s3_client.delete_object(Bucket=bucket_name, Key=file_path)
        except FileNotFoundError:
            raise ValueError("Error al eliminar el archivo")
        except NoCredentialsError:
            raise ValueError("Credenciales invalidas")
        except Exception as e:
            raise e

    @classmethod
    def get_object_s3(cls, object_name: str, string: bool = False):
        """Get an object from an S3 bucket
        :param object_name:
            Key name of the object to get
        :param string:
            True: Return string
        :return: Boto3 S3 object. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        s3_client = boto3.client('s3')
        try:
            bucket_name = Aws.get_secret('s3-fcc')['bucket_name']
            
            object = s3_client.get_object(
                Bucket=bucket_name, Key=object_name)
            object_read = object['Body'].read()
            response = object_read.decode('utf-8') if string else object_read
        except ClientError as e:
            logging.error(e)
            return None
        return response

    @classmethod
    def create_presigned_url(cls, object_name, expiration=7257600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """
        # Get S3 info
        secrets = Aws.get_secret()

        # S3 Bucket Name
        bucket_name = secrets["bucket_name"]

        # Generate a presigned URL for the S3 object
        s3_client = boto3.client('s3')
        try:
            file_valid = True
            try:
                s3_client.head_object(Bucket=bucket_name, Key=object_name)
            except:
                # raise ValueError("El archivo especificado no existe")
                file_valid = False

            if file_valid:
                response = s3_client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': bucket_name,
                        'Key': object_name},
                    ExpiresIn=expiration)
            else:
                response = None

        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response

    @classmethod
    def get_data_from_response(cls, response):
        """
        Obtener datos de la respuesta de la función lambda
        :param: response
            respuesta de la función lambda
        :return: data
        """
        response_document = response['Payload'].read().decode('utf-8')
        response_document = json.loads(response_document)
        response_body = json.loads(response_document['body'])

        return response_body
