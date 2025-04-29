import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from typing import List, Tuple, Optional

# Initialize AWS clients
ses_client = boto3.client('ses')
iam_client = boto3.client('iam')

def send_email(msg: MIMEMultipart, to_emails: List[str]) -> Optional[str]:
    """
    Sends an email using AWS SES.

    :param msg: The email message object.
    :param to_emails: A list of recipient email addresses.
    :return: The Message ID of the sent email, or None if unsuccessful.
    """
    response = ses_client.send_raw_email(
        Source=msg["From"],
        Destinations=to_emails,
        RawMessage={"Data": msg.as_string()},
    )
    return response.get('MessageId', None)

def build_msg(to_emails: List[str], from_email: str, subject_string: str, body: str) -> MIMEMultipart:
    """
    Builds an email message.

    :param to_emails: A list of recipient email addresses.
    :param from_email: The sender's email address.
    :param subject_string: The subject of the email.
    :param body: The HTML body of the email.
    :return: A MIMEMultipart email message object.
    """
    msg = MIMEMultipart()
    msg["Subject"] = subject_string
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    body_part = MIMEText(body, 'html')
    msg.attach(body_part)

    return msg

def list_access_keys(username: str) -> List[Tuple[str, date]]:
    """
    Lists access keys for a given IAM user.

    :param username: The IAM username.
    :return: A list of tuples containing AccessKeyId and CreateDate.
    """
    return [
        (item.get("AccessKeyId", ""), item.get("CreateDate", "").date())
        for item in iam_client.list_access_keys(UserName=username).get("AccessKeyMetadata", [])
    ]

def get_users() -> List[str]:
    """
    Retrieves a list of IAM user names.

    :return: A list of IAM user names.
    """
    return [item.get('UserName', "") for item in iam_client.list_users().get('Users', [])]

def get_all_access_key_with_age() -> List[Tuple[str, str, int]]:
    """
    Retrieves all IAM access keys with their age in days.

    :return: A list of tuples containing (username, access key, active days).
    """
    temp = []
    for user in get_users():
        access_key_data = list_access_keys(user)
        for keys in access_key_data:
            access_key = keys[0]
            create_date = keys[1]
            active_days = (date.today() - create_date).days
            temp.append((user, access_key, active_days))
    return temp

if __name__ == "__main__":
    FROM = "aditiyamishranit@gmail.com"
    TO = ['livingdevops@gmail.com', 'akhileshmishra121990@gmail.com']
    subject = "Access key rotation reminder"
    data = get_all_access_key_with_age()
    Expiry = 30
    for items in data:
        age = items[2]
        if age > Expiry:
            body_text = f"""
            User {items[0]} has an expiring key -> {items[1]} which is {items[2]} days old. Please rotate the access key with the following link:
            <a href="https://us-east-1.console.aws.amazon.com/iam/home?region=ap-south-1#/users/details/{items[0]}?section=security_credentials">rotate key</a>
            """
            message = build_msg(TO, FROM, subject, body_text)
            send_email(message, TO)
