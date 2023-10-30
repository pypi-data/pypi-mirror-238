import requests

from snqueue import download_from_url
from snqueue.boto3_clients import S3Client

bucket_name = "atman-uploader"
object_key = "诺华译后问题-1894573024.zip"

aws_profile_name = "terminus"

with S3Client(aws_profile_name) as s3:
  download_url = s3.create_presigned_get(bucket_name, object_key, expiration=600)
  upload_request = s3.create_presigned_post(bucket_name, "test", expiration=600)
  print(download_url)
  print(upload_request)

if download_url:
  local_filename = download_from_url(
    download_url,
    local_filename="test.zip"
  )
  print(f'File is downloaded to {local_filename}')
  with open(local_filename, 'rb') as f:
    files = {'file': (local_filename, f)}
    http_response = requests.post(
      upload_request['url'],
      data=upload_request['fields'],
      files=files
    )
  print(f'File upload HTTP status code: {http_response.status_code}')


