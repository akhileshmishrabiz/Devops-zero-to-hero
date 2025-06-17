import boto3
import json
import os
import logging
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict, Optional, Tuple
from botocore.exceptions import ClientError, BotoCoreError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Config:
    """Configuration management with validation"""
    def __init__(self):
        self.from_email = self._get_required_env('FROM_EMAIL')
        self.to_email = self._get_required_env('TO_EMAIL')
        self.expiry_days = int(os.environ.get('EXPIRY_DAYS', '90'))
        self.reminder_buffer_days = int(os.environ.get('REMINDER_BUFFER_DAYS', '5'))
        self.excluded_users = self._parse_excluded_users()
        self.aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        
        # Validation
        self.reminder_email_age = self.expiry_days - self.reminder_buffer_days
        if self.reminder_email_age <= 0:
            raise ValueError("EXPIRY_DAYS must be greater than REMINDER_BUFFER_DAYS")
    
    def _get_required_env(self, key: str) -> str:
        value = os.environ.get(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    def _parse_excluded_users(self) -> List[str]:
        excluded = os.environ.get('EXCLUDED_USERS', '')
        return [user.strip() for user in excluded.split(',') if user.strip()]

class IAMKeyRotationReminder:
    """Main class for IAM key rotation reminder functionality"""
    
    def __init__(self, config: Config):
        self.config = config
        self.iam_client = boto3.client('iam')
        self.ses_client = boto3.client('ses')
    
    def get_all_users(self) -> List[str]:
        """Retrieve all IAM users with pagination support"""
        try:
            users = []
            paginator = self.iam_client.get_paginator('list_users')
            
            for page in paginator.paginate():
                for user in page['Users']:
                    username = user['UserName']
                    if username not in self.config.excluded_users:
                        users.append(username)
            
            logger.info(f"Retrieved {len(users)} users (excluding {len(self.config.excluded_users)} excluded users)")
            return users
            
        except ClientError as e:
            logger.error(f"Error retrieving users: {e}")
            raise
    
    def get_access_keys_for_user(self, username: str) -> List[Tuple[str, int]]:
        """Get access key information for a specific user"""
        try:
            response = self.iam_client.list_access_keys(UserName=username)
            access_keys_info = []
            
            for item in response.get('AccessKeyMetadata', []):
                if item['Status'] == 'Active':
                    access_key_id = item['AccessKeyId']
                    create_date = item['CreateDate'].date()
                    age_days = (date.today() - create_date).days
                    access_keys_info.append((access_key_id, age_days))
            
            return access_keys_info
            
        except ClientError as e:
            logger.error(f"Error retrieving access keys for user {username}: {e}")
            return []
    
    def check_key_expiration(self, username: str, access_key_id: str, age_days: int) -> Optional[str]:
        """Check if access key needs rotation and return HTML message"""
        if age_days >= self.config.reminder_email_age:
            # Mask access key ID for security
            masked_key_id = f"{access_key_id[:8]}{'*' * (len(access_key_id) - 8)}"
            
            urgency_level = "CRITICAL" if age_days >= self.config.expiry_days else "WARNING"
            urgency_color = "#d32f2f" if urgency_level == "CRITICAL" else "#f57c00"
            
            return f'''
            <div style="border-left: 4px solid {urgency_color}; padding: 15px; margin: 10px 0; background-color: #f9f9f9;">
                <h3 style="color: {urgency_color}; margin: 0 0 10px 0;">{urgency_level}: Access Key Rotation Required</h3>
                <p><strong>User:</strong> {username}</p>
                <p><strong>Access Key:</strong> {masked_key_id}</p>
                <p><strong>Age:</strong> {age_days} days old</p>
                <p><strong>Action Required:</strong> {'Immediate rotation required' if urgency_level == 'CRITICAL' else 'Schedule rotation soon'}</p>
                <p style="margin-top: 15px;">
                    <a href="https://{self.config.aws_region}.console.aws.amazon.com/iam/home?region={self.config.aws_region}#/users/details/{username}?section=security_credentials" 
                       style="background-color: {urgency_color}; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px;">
                        Rotate Key Now
                    </a>
                </p>
            </div>
            '''
        return None
    
    def process_all_users(self) -> List[str]:
        """Process all users and return list of email bodies for keys needing rotation"""
        email_bodies = []
        users = self.get_all_users()
        
        total_keys_checked = 0
        keys_needing_rotation = 0
        
        for user in users:
            access_keys_info = self.get_access_keys_for_user(user)
            total_keys_checked += len(access_keys_info)
            
            for access_key_id, age_days in access_keys_info:
                email_body = self.check_key_expiration(user, access_key_id, age_days)
                if email_body:
                    email_bodies.append(email_body)
                    keys_needing_rotation += 1
        
        logger.info(f"Processed {len(users)} users, {total_keys_checked} keys checked, {keys_needing_rotation} keys need rotation")
        return email_bodies
    
    def create_email_message(self, subject: str, body_parts: List[str]) -> MIMEMultipart:
        """Create a professional email message"""
        msg = MIMEMultipart()
        msg['From'] = self.config.from_email
        msg['To'] = self.config.to_email
        msg['Subject'] = subject
        
        # Create comprehensive email body
        html_body = f'''
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #1976d2; border-bottom: 2px solid #1976d2; padding-bottom: 10px;">
                    AWS Access Key Rotation Reminder
                </h2>
                <p>The following AWS access keys require attention:</p>
                
                {''.join(body_parts)}
                
                <div style="margin-top: 30px; padding: 15px; background-color: #e3f2fd; border-radius: 4px;">
                    <h3 style="color: #1976d2; margin-top: 0;">Best Practices Reminder:</h3>
                    <ul>
                        <li>Rotate access keys regularly (every {self.config.expiry_days} days)</li>
                        <li>Delete old access keys after confirming new ones work</li>
                        <li>Use IAM roles for applications when possible</li>
                        <li>Enable AWS CloudTrail for access key usage monitoring</li>
                    </ul>
                </div>
                
                <div style="margin-top: 20px; padding: 10px; background-color: #f5f5f5; border-radius: 4px; font-size: 12px; color: #666;">
                    <p>This is an automated reminder from your AWS security monitoring system.</p>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        msg.attach(MIMEText(html_body, 'html'))
        return msg
    
    def send_email_notification(self, msg: MIMEMultipart) -> Optional[str]:
        """Send email using AWS SES with error handling"""
        try:
            response = self.ses_client.send_raw_email(
                Source=msg["From"],
                Destinations=[self.config.to_email],
                RawMessage={"Data": msg.as_string()},
            )
            message_id = response.get('MessageId')
            logger.info(f"Email sent successfully. Message ID: {message_id}")
            return message_id
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'MessageRejected':
                logger.error("Email rejected - check SES configuration and verified identities")
            elif error_code == 'SendingPausedException':
                logger.error("SES sending is paused for your account")
            else:
                logger.error(f"Failed to send email: {e}")
            raise
    
    def run_rotation_check(self) -> Dict:
        """Main method to run the rotation check"""
        try:
            email_bodies = self.process_all_users()
            
            if not email_bodies:
                logger.info("No access keys require rotation at this time")
                return {
                    'statusCode': 200,
                    'message': 'No keys require rotation',
                    'keys_processed': 0
                }
            
            # Send consolidated email
            subject = f"AWS Access Key Rotation Required - {len(email_bodies)} key(s) need attention"
            email_msg = self.create_email_message(subject, email_bodies)
            message_id = self.send_email_notification(email_msg)
            
            return {
                'statusCode': 200,
                'message': f'Rotation reminder sent for {len(email_bodies)} access keys',
                'messageId': message_id,
                'keys_processed': len(email_bodies)
            }
            
        except Exception as e:
            logger.error(f"Error in rotation check: {str(e)}")
            return {
                'statusCode': 500,
                'error': str(e)
            }

def lambda_handler(event, context):
    """Lambda entry point"""
    try:
        # Initialize configuration
        config = Config()
        logger.info("Starting IAM access key rotation check")
        
        # Run the rotation check
        reminder_service = IAMKeyRotationReminder(config)
        result = reminder_service.run_rotation_check()
        
        logger.info(f"Rotation check completed: {result}")
        return result
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {
            'statusCode': 400,
            'error': f'Configuration error: {str(e)}'
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'error': f'Unexpected error: {str(e)}'
        }

# For local testing
if __name__ == "__main__":
    test_event = {}
    test_context = {}
    result = lambda_handler(test_event, test_context)
    print(json.dumps(result, indent=2))