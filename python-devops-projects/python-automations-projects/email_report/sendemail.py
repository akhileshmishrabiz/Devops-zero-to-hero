import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ses_client = boto3.client('ses')

FROM = "aditiyamishranit@gmail.com"
TO = ['livingdevops@gmail.com', 'akhileshmishra121990@gmail.com']

subject = "this is the subject of email from python - html"
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

msg = MIMEMultipart()
msg["Subject"] = subject
msg["From"] = FROM
msg["To"] = ", ".join(TO)
# body_part = MIMEText(body, "plain")
part1 = MIMEText(body_text, 'plain')
part2 = MIMEText(body_text, 'html')
msg.attach(part2)

response = ses_client.send_raw_email(
    Source=msg["From"],
    Destinations=TO,
    RawMessage={"Data": msg.as_string()},
)

print(response)
