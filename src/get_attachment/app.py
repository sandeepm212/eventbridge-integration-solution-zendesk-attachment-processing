import os
import json
import boto3
import logging
import requests
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def lambda_handler(event, context):

    accepted_content_types = ['image/png', 'image/jpeg', 'application/jpeg', 'application/pdf', 'jpeg', 'png', 'pdf']

    if event['detail']['ticket_event']['attachment']['content_type'] in accepted_content_types:
      attachment_data = extract_attachment_data(event)

      attachment_data['bucket_key'] = f"{attachment_data['file_name']}/{attachment_data['attachment_id']}"

      upload_to_s3(attachment_data)

    else:
      return {
        'accepted_file_type': False
      }

    return {
      'accepted_file_type': True,
      'attachment_data': attachment_data
    }

def extract_attachment_data(event):

  attachment_data = {
    'ticket_id': event['detail']['ticket_event']['ticket']['id'],
    'attachment_id': event['detail']['ticket_event']['attachment']['id'],
    'content_type': event['detail']['ticket_event']['attachment']['content_type'],
    'url': event['detail']['ticket_event']['attachment']['content_url'],
    'file_name': event['detail']['ticket_event']['attachment']['filename']
  }

  return attachment_data

def upload_to_s3(attachment_data):

    r = requests.get(attachment_data['url'], stream=True)

    try:
        s3_client.upload_fileobj(r.raw, os.environ['S3_BUCKET'], attachment_data['bucket_key'])
    except ClientError as e:
        logging.error(e)
        raise e
    
    return