import sys
sys.path.append('../../')

import os
import json
import unittest
from unittest import mock

with mock.patch.dict('os.environ', {'AWS_REGION': 'us-west-2'}):
  from get_text.app import lambda_handler

def mocked_textract_call(attachment_data):
    return {
      "Blocks":
      [
        {
          "BlockType": "LINE",
          "Text": "Sample text 1"
        },
        {
          "BlockType": "LINE",
          "Text": "Sample text 2"
        }
      ]
    }

def mocked_textract_call_no_text(attachment_data):
    return {
      "Blocks": []
    }

class GetTextTest(unittest.TestCase):

  @mock.patch('get_text.app.textract_detect_text', side_effect=mocked_textract_call)
  def test_build(self, call_textract_mock):

    output = self.get_step_function_output()
    response = lambda_handler(self.get_step_function_output(), "")

    self.assertEqual(call_textract_mock.call_count, 1)
    self.assertEqual(response['text_detected'], True)
    self.assertIn('attachment_text', response)
    self.assertIn('attachment_data', response)
    self.assertEqual(response['attachment_data']['ticket_id'], output['attachment_data']['ticket_id'])
    self.assertEqual(response['attachment_data']['attachment_id'], output['attachment_data']['attachment_id'])
    self.assertEqual(response['attachment_data']['content_type'], output['attachment_data']['content_type'])
    self.assertEqual(response['attachment_data']['url'], output['attachment_data']['url'])
    self.assertEqual(response['attachment_data']['file_name'], output['attachment_data']['file_name'])
    self.assertEqual(response['attachment_data']['bucket_key'], output['attachment_data']['bucket_key'])

  @mock.patch('get_text.app.textract_detect_text', side_effect=mocked_textract_call_no_text)
  def test_no_text_found(self, call_textract_mock):

    output = self.get_step_function_output()
    response = lambda_handler(self.get_step_function_output(), "")

    self.assertEqual(call_textract_mock.call_count, 1)
    self.assertEqual(response['text_detected'], False)
    self.assertNotIn('attachment_text', response)
    self.assertIn('attachment_data', response)
    self.assertEqual(response['attachment_data']['ticket_id'], output['attachment_data']['ticket_id'])
    self.assertEqual(response['attachment_data']['attachment_id'], output['attachment_data']['attachment_id'])
    self.assertEqual(response['attachment_data']['content_type'], output['attachment_data']['content_type'])
    self.assertEqual(response['attachment_data']['url'], output['attachment_data']['url'])
    self.assertEqual(response['attachment_data']['file_name'], output['attachment_data']['file_name'])
    self.assertEqual(response['attachment_data']['bucket_key'], output['attachment_data']['bucket_key'])

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