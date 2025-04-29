import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

# Create an SES client
ses_client = boto3.client('ses')

def send_email(msg: MIMEMultipart, to_emails: List[str]) -> Optional[str]:
    """
    Send an email using AWS SES.

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
    Build an email message.

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

if __name__ == "__main__":
    FROM = "aditiyamishranit@gmail.com"
    TO = ['livingdevops@gmail.com', 'akhileshmishra121990@gmail.com']

    subject = "This is the subject of email from Python - HTML"
    body_text = """
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #4CAF50;">Send Email with AWS SES</h2>
        <ol>
            <li>Install Boto3: <code style="background-color: #f0f0f0; padding: 2px;">pip install boto3</code></li>
            <li>Configure AWS credentials.</li>
            <li>Use the following Python code:</li>
        </ol>
        <pre style="background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd;">
    <code style="color: #d14;">import</code> boto3
    ses = boto3.client(<code style="color: #690;">'ses'</code>, region_name=<code style="color: #690;">'your-region'</code>)
    ses.send_email(Source=<code style="color: #690;">'sender@example.com'</code>,
                   Destination={ <code style="color: #d14;">'ToAddresses'</code>: [<code style="color: #690;">'recipient@example.com'</code>]},
                   Message={ <code style="color: #d14;">'Subject'</code>: {<code style="color: #d14;">'Data'</code>: <code style="color: #690;">'Subject'</code>},
                            <code style="color: #d14;">'Body'</code>: {<code style="color: #d14;">'Text'</code>: {<code style="color: #d14;">'Data'</code>: <code style="color: #690;">'Hello from SES'</code>}}})
        </pre>
    </body>
    </html>
    """
    message = build_msg(TO, FROM, subject, body_text)
    send_email(message, TO)
