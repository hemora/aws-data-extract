# aws-data-extract

Script para extraer datos del bucket de AWS

## Instrucciones

1. Generar un usuario usando el servicio IAM de AWS con las políticas necesarias para poder listar y descargar los objetos del bucket 
(e.g.)
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::<bucket>"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectAcl"
            ],
            "Resource": "arn:aws:s3:::<bucket>/*"
        }
    ]
}
```
2. Crear las credenciales de acceso para el usuario creado y descargarlas:
![image](https://github.com/user-attachments/assets/b18b2f32-7b20-4e02-a705-532d4c2c8aff)

3. Trasladarse a donde se descargarán los datos.
4. Ejecutar el script (i.e.) `python3 aws_data_extract.py`
5. Aparecerán prompts solicitando el nombre y prefijo del bucket, y las credenciales de acceso descargadas (por default los inputs no son mostrados en la terminal).
6. Si la configuración de acceso es exitosa se mostrará un listado de los objetos y los directorios presentes en el bucket así como sus tamaños aproximados en GB. 
La salida completa también podrá encontrarse en un archivo con nombre `directory_info.txt` para su consulta.
7. Se le preguntará al usuario si desea proceder con la descarga de los objetos.
8. En caso de aceptar se iniciará la descarga y se generará un archivo `downloaded.txt` en donde se podrá consultar los objetos que han sido descargados.

