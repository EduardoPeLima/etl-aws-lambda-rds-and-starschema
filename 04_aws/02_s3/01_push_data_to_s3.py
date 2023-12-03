import boto3 
import os

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

def get_s3_client():
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    print("Connected to AWS")
    return s3_client

def ensure_s3_bucket_exists(s3_client, BUCKET_NAME):
    try:
        try:
            s3_client.head_bucket(Bucket=BUCKET_NAME)
        except:
            s3_client.create_bucket(
                Bucket=BUCKET_NAME,
            )
            print(f'Bucket {BUCKET_NAME} created')
        else:
            print(f'bucket {BUCKET_NAME} already exists')
        
    except Exception as e:
        print(f'Failed to create bucket: {e}')

def send_folder_data_to_s3(s3_client, BUCKET_NAME, folder_path):
    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)
        s3_client.upload_file(file_path, BUCKET_NAME, file)
        print(f'{file} uploaded to S3')
    
    print('All files were uploaded to S3')


s3_client = get_s3_client()
ensure_s3_bucket_exists(s3_client, BUCKET_NAME)
send_folder_data_to_s3(s3_client, BUCKET_NAME, '02_northwind_exported_relational_data_files')



