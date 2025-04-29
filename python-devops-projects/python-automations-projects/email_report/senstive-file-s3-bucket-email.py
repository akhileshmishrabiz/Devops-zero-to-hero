# find the .pem if exist and send the email to the user
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

s3_client = boto3.client('s3')
ses_client = boto3.client('ses')
admin = "akhileshmishrabiz@gmail.com"
team =  "akhileshmishra121990@gmail.com"

def list_bucket(region):
    response = s3_client.list_buckets(
        BucketRegion=region
    )
    temp = []
    for bucket in response.get('Buckets'):
        bucket_name = bucket.get('Name', "Key dont exist")
        temp.append(bucket_name)
    return temp

def list_bucket_objects(bucket_name):
    bucket_pbject = s3_client.list_objects(
        Bucket=bucket_name,
    )
    temp = []
    for i in bucket_pbject.get("Contents", []):
        object = i.get("Key")
        temp.append(object)
    return temp
def get_bucket_owner_email(bucket_name):
   try:
       s3_client = boto3.client('s3')
       response = s3_client.get_bucket_tagging(Bucket=bucket_name)
       bucket_owner_email = None
       
       if not bucket_owner_email:
           for tag in response.get('TagSet', []):
               if tag['Key'].lower() == 'bucket_owner' or tag['Key'].lower() == 'account_owner':
                   bucket_owner_email = tag['Value']
                   break
            
       
       if not bucket_owner_email:
           bucket_owner_email = "livingdevops@gmail.com"
           
       return bucket_owner_email
   
   except Exception as e:
       return "livingdevops@gmail.com"

def get_data_for_email(region):
    buckets = list_bucket(region)
    temp = []
    for bucket in buckets:
        owner = get_bucket_owner_email(bucket)
        for items in list_bucket_objects(bucket):
            ext = items.split(".")[-1]
            if ext == "pem":
                temp.append((bucket,owner, items))
    return temp

def process_lambda(region):
    for items in get_data_for_email(region):
       bucket, owner, file = items
    #    print(f"Bucket: {bucket} , Owner: {owner} , File: {file}")
       message = build_email(bucket, file, owner,admin, region)
       From = message["From"]
       To = message["To"]
       message = message
       send_email(From, To, message)

def send_email(From, To, Message):
    # Convert To to a list if it's a string
    destinations = To.split(', ') if isinstance(To, str) else To
    
    response = ses_client.send_raw_email(
        Source=From,
        Destinations=destinations,
        RawMessage={"Data": Message.as_string()},
    )
    print(response)
    return response.get('MessageId', None)
    
def build_email(bucket, file, owner,admi, region):
    bucket_link = f"https://{region}.console.aws.amazon.com/s3/buckets/{bucket}?region={region}&bucketType=general&tab=objects"
    body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
                <h2 style="color: #c41e3a;">⚠️ Security Alert: Sensitive File Detected</h2>
                <p>We have detected a sensitive <strong>.pem</strong> file in your S3 bucket that requires immediate attention:</p>
                <ul>
                    <li><strong>Bucket:</strong> <a href="{bucket_link}" style="color: #0066cc;">{bucket}</a></li>
                    <li><strong>File:</strong> {file}</li>
                </ul>
                <p>Please delete this file immediately as it may pose a security risk.</p>
                <div style="background-color: #f8f8f8; padding: 15px; border-left: 4px solid #c41e3a; margin: 20px 0;">
                    <p style="margin: 0;"><strong>Recommendation:</strong> Remove the .pem file and review your bucket for other sensitive content.</p>
                </div>
                <p>If you have any questions, please contact the security team.</p>
                <p style="font-size: 12px; color: #666; margin-top: 30px;">This is an automated security notification.</p>
            </div>
        </body>
        </html>
        """

    msg = MIMEMultipart()
    msg["Subject"] = f" !!IMPORTANT : Senstive file in your bucket"
    msg["From"] = admin
    to_emails = [owner]
    msg["To"] = ", ".join(to_emails)
    body_part = MIMEText(body, 'html')
    msg.attach(body_part)
    return  msg


def lambda_handler(event, context):
    # fetch the region from the event
    region = event.get("region")
    return process_lambda(region)

# process_lambda("ap-south-1")

