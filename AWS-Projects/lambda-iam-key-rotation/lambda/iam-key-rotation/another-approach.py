import os
import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class Config:
    """Configuration management using environment variables"""
    
    def __init__(self):
        self.rotation_threshold_days = int(os.getenv('ROTATION_THRESHOLD_DAYS', '90'))
        self.warning_threshold_days = int(os.getenv('WARNING_THRESHOLD_DAYS', '80'))
        self.sns_topic_arn = os.getenv('SNS_TOPIC_ARN')
        self.excluded_users = self._parse_excluded_users()
        self.notification_template = os.getenv('NOTIFICATION_TEMPLATE', 'default')
        self.dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        
    def _parse_excluded_users(self) -> List[str]:
        """Parse comma-separated list of users to exclude"""
        excluded = os.getenv('EXCLUDED_USERS', '')
        return [user.strip() for user in excluded.split(',') if user.strip()]

def lambda_handler(event, context):
    """
    Main Lambda handler for access key rotation reminders
    """
    config = Config()
    
    try:
        # Initialize AWS clients
        iam_client = boto3.client('iam')
        sns_client = boto3.client('sns')
        
        # Get access key information
        access_keys_info = get_all_access_keys(iam_client, config.excluded_users)
        
        # Identify keys requiring attention
        keys_to_notify = analyze_key_ages(
            access_keys_info, 
            config.rotation_threshold_days,
            config.warning_threshold_days
        )
        
        # Send notifications
        if keys_to_notify and not config.dry_run:
            send_notifications(sns_client, keys_to_notify, config)
        
        # Return execution summary
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Access key rotation check completed',
                'keys_analyzed': len(access_keys_info),
                'notifications_sent': len(keys_to_notify),
                'dry_run': config.dry_run
            })
        }
        
    except Exception as e:
        print(f"Error in lambda execution: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_all_access_keys(iam_client, excluded_users: List[str]) -> List[Dict]:
    """
    Retrieve all access keys from IAM, excluding specified users
    """
    access_keys = []
    
    try:
        # Get all IAM users
        paginator = iam_client.get_paginator('list_users')
        
        for page in paginator.paginate():
            for user in page['Users']:
                username = user['UserName']
                
                # Skip excluded users
                if username in excluded_users:
                    continue
                
                # Get access keys for each user
                keys_response = iam_client.list_access_keys(UserName=username)
                
                for key in keys_response['AccessKeyMetadata']:
                    access_keys.append({
                        'username': username,
                        'access_key_id': key['AccessKeyId'],
                        'created_date': key['CreateDate'],
                        'status': key['Status'],
                        'age_days': (datetime.now(key['CreateDate'].tzinfo) - key['CreateDate']).days
                    })
                    
    except Exception as e:
        print(f"Error retrieving access keys: {str(e)}")
        raise
    
    return access_keys

def analyze_key_ages(access_keys: List[Dict], rotation_threshold: int, warning_threshold: int) -> List[Dict]:
    """
    Analyze access key ages and categorize them for notifications
    """
    keys_requiring_action = []
    
    for key_info in access_keys:
        age_days = key_info['age_days']
        
        # Skip inactive keys
        if key_info['status'] != 'Active':
            continue
            
        notification_type = None
        urgency = 'low'
        
        if age_days >= rotation_threshold:
            notification_type = 'overdue'
            urgency = 'high'
        elif age_days >= warning_threshold:
            notification_type = 'warning'
            urgency = 'medium'
        
        if notification_type:
            keys_requiring_action.append({
                **key_info,
                'notification_type': notification_type,
                'urgency': urgency,
                'days_overdue': max(0, age_days - rotation_threshold)
            })
    
    return keys_requiring_action

def send_notifications(sns_client, keys_to_notify: List[Dict], config: Config) -> None:
    """
    Send SNS notifications for access keys requiring rotation
    """
    # Group notifications by user
    user_notifications = {}
    
    for key_info in keys_to_notify:
        username = key_info['username']
        if username not in user_notifications:
            user_notifications[username] = []
        user_notifications[username].append(key_info)
    
    # Send notification for each user
    for username, user_keys in user_notifications.items():
        message = create_notification_message(username, user_keys, config.notification_template)
        
        try:
            sns_client.publish(
                TopicArn=config.sns_topic_arn,
                Subject=f"AWS Access Key Rotation Required - {username}",
                Message=message
            )
            print(f"Notification sent for user: {username}")
            
        except Exception as e:
            print(f"Failed to send notification for {username}: {str(e)}")

def create_notification_message(username: str, keys: List[Dict], template: str) -> str:
    """
    Create formatted notification message
    """
    if template == 'detailed':
        return create_detailed_message(username, keys)
    else:
        return create_standard_message(username, keys)

def create_standard_message(username: str, keys: List[Dict]) -> str:
    """Create standard notification message"""
    overdue_keys = [k for k in keys if k['notification_type'] == 'overdue']
    warning_keys = [k for k in keys if k['notification_type'] == 'warning']
    
    message = f"Hello {username},\n\n"
    message += "Your AWS access keys require attention:\n\n"
    
    if overdue_keys:
        message += "🔴 OVERDUE - Immediate Action Required:\n"
        for key in overdue_keys:
            message += f"  • Key: {key['access_key_id'][:8]}*** (Age: {key['age_days']} days)\n"
        message += "\n"
    
    if warning_keys:
        message += "🟡 WARNING - Rotation Recommended:\n"
        for key in warning_keys:
            message += f"  • Key: {key['access_key_id'][:8]}*** (Age: {key['age_days']} days)\n"
        message += "\n"
    
    message += "Please rotate these keys as soon as possible to maintain security best practices.\n"
    message += "\nFor key rotation instructions, visit: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html"
    
    return message

def create_detailed_message(username: str, keys: List[Dict]) -> str:
    """Create detailed notification message with additional context"""
    message = create_standard_message(username, keys)
    message += "\n\n--- Additional Information ---\n"
    message += f"Total keys analyzed: {len(keys)}\n"
    message += f"Notification generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    
    return message