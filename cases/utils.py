import boto3
from botocore.exceptions import ClientError
from django.conf import settings

class AwsHandler:
    @classmethod
    def get_file_tmp_url(cls, file_path):
        try:
           s3_client = boto3.client(
               's3',
               endpoint_url=settings.AWS_S3_ENDPOINT_URL,
               aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
           )
        except Exception as exc:
           return None
        else:
           try:
               bucket = settings.AWS_STORAGE_BUCKET_NAME
               # Note: Your settings say location="media", so the key usually includes media/
               # ensure file_path doesn't already start with media/ to avoid duplication
               object_name = "media/" + str(file_path)

               response = s3_client.generate_presigned_url(
                   'get_object',
                   Params={
                       'Bucket': bucket,
                       'Key': object_name
                   },
                   ExpiresIn=3600
               )
               return response
           except ClientError as e:
               return None
