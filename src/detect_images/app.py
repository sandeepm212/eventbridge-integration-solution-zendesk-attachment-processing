import os
import boto3

rekognition_client = boto3.client('rekognition', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):

  attachment_data = event['attachment_data']

  response = rekognition_detect_labels(attachment_data)

  images_found = []
  main_images_found = []

  for item in response['Labels']:
    images_found.append(item['Name'])
  
  # If no text detected, set labels_detected to False
  if len(images_found) == 0:
    labels_detected = False

    return {
    'image_labels_detected': labels_detected,
    }

  # If text detected, include up to 5 image labels
  else:
    labels_detected = True
    main_images_found = images_found[:5]
    image_string = ", ".join(main_images_found)

  return {
    'image_labels_detected': labels_detected,
    'attachment_images': image_string
  }

def rekognition_detect_labels(attachment_data):

  response = rekognition_client.detect_labels(
      Image={'S3Object': {'Bucket': os.environ['S3_BUCKET'], 'Name': attachment_data['bucket_key']}})
  
  return response


