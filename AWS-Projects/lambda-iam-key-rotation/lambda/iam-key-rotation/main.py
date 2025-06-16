import boto3
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


username = "cliuser-akhilesh" 
Expiry_days = 20
reminder_email_age = Expiry_days - 5

def get_users():
    iam_client = boto3.client('iam')
    response = iam_client.list_users()
    return [user['UserName'] for user in response['Users']]


def get_access_keys_age(username):
    iam_client = boto3.client('iam')
    response = iam_client.list_access_keys(UserName=username).get('AccessKeyMetadata', [])
    
    access_keys_info = []
    for item in response:
        if item['Status'] == 'Active':
            access_key_id = item['AccessKeyId']
            create_date = item['CreateDate'].date()
            age = (date.today() - create_date).days
            access_keys_info.append((access_key_id, age))
    
    return access_keys_info

def if_key_expired(access_key_id, age, reminder_email_age):
    if age >= reminder_email_age:
        return f'''
    <p>Reminder: Access key <strong>{access_key_id}</strong> is <strong>{age}</strong> days old. Please rotate it.</p>
    <p>For more details, visit the <a href="https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/users/details/{username}?section=security_credentials"> Rotate this key here</a>.</p>
    '''
    return None

def process_users():
    email_body_list = []
    users = get_users()
    for user in users:
        access_keys_info = get_access_keys_age(user)
        for keys in access_keys_info:
            access_key_id, age = keys   
            email_body = if_key_expired(access_key_id, age, reminder_email_age)
            if email_body:
                email_body_list.append(email_body)       
    return email_body_list
            
def build_email_message(to_email, from_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body_part = MIMEText(body, 'html')
    msg.attach(body_part)

    return msg

def send_email(msg, to_emails):
    ses_client = boto3.client('ses')
    response = ses_client.send_raw_email(
        Source=msg["From"],
        Destinations=to_emails,
        RawMessage={"Data": msg.as_string()},
    )
    return response.get('MessageId', None)

def main(event, context):
    subject = f"AWS Access Key Rotation Reminder -user {username}"
    to_email = "aditiyamishranit@gmail.com"
    from_email = "akhileshmishra121990@gmail.com"
    for email_body in process_users():
        email_msg = build_email_message(to_email, from_email, subject, email_body)
        email_sent =send_email(email_msg, [to_email])
        print(f"Email sent with Message ID: {email_sent}")
