import os
import json
from zenpy.lib.api_objects import Comment
from zenpy import Zenpy #importing zenpy (https://github.com/facetoe/zenpy)

def lambda_handler(event, context):

  output = merge_branch_output(event)

  text_detected_body, images_detected_body = assemble_message_body(output)

  zenpy_update_ticket(output, text_detected_body, images_detected_body)

  return

def merge_branch_output(event):

  text_branch_output = event[0]
  image_branch_output = event[1]

  output = {**text_branch_output, **image_branch_output}

  return output

def assemble_message_body(output):

  if output['image_labels_detected'] == True:
    images_detected_body = f"Main images detected: {output['attachment_images']}"
  else: 
    images_detected_body = "No images detected"
  
  if output['text_detected'] == True: 
    text_detected_body = f"Text detected: {output['attachment_text']}"
  else:
    text_detected_body = "No text detected"

  return text_detected_body, images_detected_body

def zenpy_update_ticket(output, text_detected_body, images_detected_body):
  
  credentials = {
      'email': os.environ['ZENDESK_EMAIL'],
      'token': os.environ['ZENDESK_TOKEN'],
      'subdomain': os.environ['ZENDESK_SUBDOMAIN']
  }

  zenpy_client = Zenpy(**credentials)

  ticket = zenpy_client.tickets(id=output['attachment_data']['ticket_id'])
  
  ticket.comment = Comment(body=text_detected_body, html_body='<h4>Attachment processed by Amazon Textract & Amazon Rekognition</h4><p>{}<p><p>{}</p>'.format(images_detected_body, text_detected_body), public=False)
  
  zenpy_client.tickets.update(ticket)

  return