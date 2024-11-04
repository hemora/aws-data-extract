import boto3
from boto3.s3.transfer import TransferConfig

from dotenv import load_dotenv
load_dotenv()
import os

import getpass

import sys

def configure_credentials(access_key: str, secret_access_key: str, region: str) :
    """
    """
    s3_client = boto3.client(
        "s3"
        , aws_access_key_id = access_key
        , aws_secret_access_key = secret_access_key
        , region_name = region
    )

    s3_resource = boto3.resource(
        "s3"
        , aws_access_key_id = access_key
        , aws_secret_access_key = secret_access_key
        , region_name = region
    )

    return s3_client, s3_resource

def get_engine(access_key: str, secret_access_key: str, region: str) :
    """
    """
    s3_resource = boto3.resource(
        "s3"
        , aws_access_key_id = access_key
        , aws_secret_access_key = secret_access_key
        , region_name = region
    )

    return s3_resource

def list_bucket_info(s3_client, bucket_name: str, prefix: str):
    """
    """
    response = s3_client.list_objects(
        Bucket=bucket_name
        , Prefix=prefix
    )

    total_size = 0
    entry = ""
    info_text = ""
    for element in response["Contents"]:
        if element.get("Key").endswith("/"):
            entry = f"[Directorio] {element.get('Key')}"
            
        else:
            entry = f"[Objeto] {element.get('Key')}"

        info_text += f"{entry}\n"
        print(entry)
        
        entry = f" > Tamaño (en GB) {element.get('Size') / 1073741824}"
        info_text += f"{entry}\n"
        print(entry)

        total_size += element.get("Size") / 1073741824

    print("==========================================")
    info_text += "==========================================\n"
    entry = "Tamaño total " + str(total_size) + " GB"
    print(entry)
    info_text += f"{entry}\n"

    return info_text

if __name__ == "__main__":

    AWS_BUCKET = input("Ingresar bucket: ")
    AWS_PREFIX = input("Ingresar prefijo: ")
    if AWS_PREFIX.endswith('/'):
        AWS_PREFIX = AWS_PREFIX + "country=MEX/year=2024"
    else:
        AWS_PREFIX = AWS_PREFIX + "/country=MEX/year=2024"

    # Configure the credentials
    print("========== Ingresar Credenciales ======")
    access_key = getpass.getpass("Acess Key: ")
    secret_access_key = getpass.getpass("Secret Acess Key: ")
    region = getpass.getpass("Region [us-east-1]:")
    if region == "":
        region = "us-east-1"

    print(region)

    s3_client, s3_resource = \
        configure_credentials(access_key, secret_access_key, region)
    
    info = list_bucket_info(s3_client, AWS_BUCKET, AWS_PREFIX)
    print("Se generó un archivo de texto con el output completo para su consulta.")
    with open("./directory_info.txt", "w+") as f:
        f.write(info)

    decision = input("Quiere descargar los datos? [y/n]: ")
    if decision == "y" or decision == "":

        # Descargar datos
        bucket = s3_resource.Bucket(AWS_BUCKET)
        object_list = \
            [obj.key for obj in bucket.objects.filter(Prefix=AWS_PREFIX) \
             if not obj.key.endswith('/')]

        print(object_list)

        config = TransferConfig(
            multipart_threshold=1024 * 100,
            max_concurrency=10,
            multipart_chunksize=1024 * 100,
            use_threads=True,
        )

        for obj in object_list:
            if not os.path.exists(os.path.dirname(obj)):
                os.makedirs(os.path.dirname(obj))
            try:
                bucket.download_file(obj, obj, Config=config) 
            except Exception as e:
                print(e)

            with open("./downloaded.txt", "a") as f:
                f.write(obj + "\n")

    elif decision == "n":
        sys.exit("Programa finalizado")
    else:
        sys.exit()
