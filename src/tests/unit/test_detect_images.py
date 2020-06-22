import sys
sys.path.append('../../')

import os
import json
import unittest
from unittest import mock

with mock.patch.dict('os.environ', {'AWS_REGION': 'us-west-2'}):
  from detect_images.app import lambda_handler

def mocked_rekognition_call(attachment_data):
    return {
      "Labels":
      [
        {
          "Name": "Example label 1"
        },
        {
          "Name": "Example label 2"
        }
      ]
    }

def mocked_rekognition_call_no_labels(attachment_data):
    return {
      "Labels": []
    }

class DetectImageTest(unittest.TestCase):

  @mock.patch('detect_images.app.rekognition_detect_labels', side_effect=mocked_rekognition_call)
  def test_build(self, call_rekognition_mock):

    output = self.get_step_function_output()
    response = lambda_handler(self.get_step_function_output(), "")

    self.assertEqual(call_rekognition_mock.call_count, 1)
    self.assertEqual(response['image_labels_detected'], True)
    self.assertIn('attachment_images', response)

  @mock.patch('detect_images.app.rekognition_detect_labels', side_effect=mocked_rekognition_call_no_labels)
  def test_no_labels_found(self, call_rekognition_mock):

    output = self.get_step_function_output()
    response = lambda_handler(self.get_step_function_output(), "")

    self.assertEqual(call_rekognition_mock.call_count, 1)
    self.assertEqual(response['image_labels_detected'], False)
    self.assertNotIn('attachment_images', response)


  def get_step_function_output(self):
    return {   
      "accepted_file_type":True,
      "attachment_data":
      {
        "ticket_id":53,
        "attachment_id":376856773391,
        "content_type":"image/png",
        "url":"https://subdomain.zendesk.com/attachments/token/1234/?name=image.png",
        "file_name":"image.png",
        "bucket_key":"image.png/376856773391"
      }
    }

if __name__ == '__main__':
    unittest.main()