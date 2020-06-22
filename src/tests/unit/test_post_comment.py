import sys
sys.path.append('../../')

import os
import json
import unittest
from unittest import mock

from post_comment.app import lambda_handler

# In order to run this test, zenpy needs to be installed
# Importing zenpy (https://github.com/facetoe/zenpy)
def mocked_zenpy_update_ticket(output, text_detected_body, images_detected_body):
    return

class PostCommentTest(unittest.TestCase):

  @mock.patch('post_comment.app.zenpy_update_ticket', side_effect=mocked_zenpy_update_ticket)
  def test_build(self, update_ticket_mock):

    response = lambda_handler(self.get_step_function_output(), "")

    self.assertEqual(update_ticket_mock.call_count, 1)

  def get_step_function_output(self):
    return [
      {
          "text_detected": True,
          "attachment_text":"Sample text 1 Sample text 2",
          "attachment_data":
          {
            "ticket_id":53,
            "attachment_id":376856773391,
            "content_type":"image/png",
            "url":"https://subdomain.zendesk.com/attachments/token/1234/?name=image.png",
            "file_name":"image.png",
            "bucket_key":"image.png/376856773391"
          }
      },
      {
          "image_labels_detected": True,
          "attachment_images":"Example label 1, Example label 2"
      }
    ]

if __name__ == '__main__':
    unittest.main()