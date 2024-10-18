import boto3
import os

def handler(event, context):
    # Create an S3 client
    s3_client = boto3.client('s3')
    bucket_path = os.getenv('BUCKET_PATH')
    print(f'Bucket path: {bucket_path}')
    bucket_name = bucket_path.split('/')[0]
    prefix = bucket_path.split(bucket_name + '/')[1]

    print(f'Bucket name: {bucket_name} and prefix: {prefix}')

    # # List all the files in the specified path
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')['Contents']

    try:
    # Iterate over the objects and print their names
        for obj in response:
            if obj['Key'] != prefix:
                filename_path = obj['Key']
                year = filename_path.split('.txt')[0].split('-')[2]
                month = filename_path.split('.txt')[0].split('-')[3]
                date   = filename_path.split('.txt')[0].split('-')[4]
                new_filename = filename_path.split('incoming/')[1]
                new_path = f"{prefix}{year}/{month}/{date}/{new_filename}"
                
                print(f'Filename: {filename_path} and new_filename: {new_path}')
                # Copy the file to the new path
                s3_client.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': filename_path},
                    Key=new_path
                )
                
                # Delete the original file
                s3_client.delete_object(Bucket=bucket_name, Key=filename_path)
                
                print(f'Moved file: {filename_path} to {new_path}')
    except Exception as e:
        print(e)

# # Run the function
if __name__ == '__main__':
    handler("", "")