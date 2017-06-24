import boto3
from wand.image import Image

def lambda_handler(event, context):
    bucket   = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    tmp_path = '/tmp/' + filename
    client   = boto3.client('s3')
    client.download_file(bucket, filename, tmp_path)

    with Image(filename = tmp_path, resolution = 600) as img:
        filename = filename.replace('.pdf', '.jpg')
        tmp_path = '/tmp/' + filename

        img.format        = 'jpeg'
        img.alpha_channel = False

        img.transform(resize = '1920x')
        img.save(filename = tmp_path)

    client.upload_file(tmp_path, bucket, filename)
