import os
import boto3

textract_client = boto3.client('textract', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):

  attachment_data = event['attachment_data']

  response = textract_detect_text(attachment_data)

  text_found = []

  for block in response['Blocks']:
    if block['BlockType'] == "LINE":
      text_found.append(block['Text'])
  
  # If no text detected, set text_detected to False
  if len(text_found) == 0:
    text_detected = False

    return {
    'text_detected': text_detected,
    'attachment_data': attachment_data
  }

  # If text detected, concatenate lines of text
  else:
    text_detected = True
    concatenated_text = " ".join(text_found)

  return {
    'text_detected': text_detected,
    'attachment_text': concatenated_text,
    'attachment_data': attachment_data
  }

def textract_detect_text(attachment_data):

  response = textract_client.detect_document_text(
      Document={'S3Object': {'Bucket': os.environ['S3_BUCKET'], 'Name': attachment_data['bucket_key']}})

  return response
