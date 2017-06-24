import boto3
import subprocess

def lambda_handler(event, context):
    bucket   = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    tmp_path = '/tmp/' + filename
    client   = boto3.client('s3')
    client.download_file(bucket, filename, tmp_path)

    out_file = filename.replace('.pdf', '.jpg')
    out_path = tmp_path.replace('.pdf', '.jpg')

    cmd  = 'convert '
    cmd += '-density 300 '
    cmd += '-colorspace RGB '
    cmd += '-alpha Remove '
    cmd += '-scale 1920x '
    cmd += '-quality 80 '
    cmd += '-append '
    cmd += tmp_path
    cmd += ' '
    cmd += out_path
    subprocess.call(cmd.strip().split(' '))

    client.upload_file(out_path, bucket, out_file)
