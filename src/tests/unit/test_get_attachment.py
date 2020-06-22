import sys
sys.path.append('../../')

import os
import json
import unittest
from unittest import mock

from get_attachment.app import lambda_handler

def mocked_upload_to_s3(attachment_data):
    return

class GetAttachmentTest(unittest.TestCase):

  @mock.patch('get_attachment.app.upload_to_s3', side_effect=mocked_upload_to_s3)
  def test_build(self, s3_upload_mock):

    event_type = "supported_file_type_attached"
    event = self.get_eventbridge_event(event_type)
    response = lambda_handler(self.get_eventbridge_event(event_type), "")

    self.assertEqual(s3_upload_mock.call_count, 1)
    self.assertEqual(response['accepted_file_type'], True)
    self.assertIn('attachment_data', response)
    self.assertEqual(response['attachment_data']['ticket_id'], event['detail']['ticket_event']['ticket']['id'])
    self.assertEqual(response['attachment_data']['attachment_id'], event['detail']['ticket_event']['attachment']['id'])
    self.assertEqual(response['attachment_data']['content_type'], event['detail']['ticket_event']['attachment']['content_type'])
    self.assertEqual(response['attachment_data']['url'], event['detail']['ticket_event']['attachment']['content_url'])
    self.assertEqual(response['attachment_data']['file_name'], event['detail']['ticket_event']['attachment']['filename'])
    self.assertIn('bucket_key', response['attachment_data'])

  @mock.patch('get_attachment.app.upload_to_s3', side_effect=mocked_upload_to_s3)
  def test_unsupported_file_type(self, s3_upload_mock):

    event_type = "unsupported_file_type_attached"
    response = lambda_handler(self.get_eventbridge_event(event_type), "")

    self.assertEqual(response['accepted_file_type'], False)

  def get_eventbridge_event(self, event_type):
      if event_type == 'supported_file_type_attached':
          return {
              "version":"0",
              "id":"7e784552-fceb-eb6c-5598-cf0a301a64a7",
              "detail-type":"Support Ticket: Attachment Linked to Comment",
              "source":"aws.partner/zendesk.com/1234/default",
              "account":"426339633214",
              "time":"2020-06-15T05:32:28Z",
              "region":"us-west-2",
              "resources":[
                  "Support Ticket"
              ],
              "detail":{
                  "ticket_event":{
                    "meta":{
                        "version":"1.0",
                        "occurred_at":"2020-06-15T05:32:26Z",
                        "ref":"21-461478505",
                        "sequence":{
                          "id":"99246BC29B2E62BDA0DD85CF17977BB9",
                          "position":1,
                          "total":2
                        }
                    },
                    "type":"Attachment Linked to Comment",
                    "attachment":{
                        "id":376856773391,
                        "content_url":"https://subdomain.zendesk.com/attachments/token/1234/?name=image.png",
                        "content_type":"image/png",
                        "filename":"image.png",
                        "is_public":True,
                        "comment_id":1088758661652
                    },
                    "ticket":{
                        "id":53,
                        "created_at":"2020-06-14T19:20:39Z",
                        "updated_at":"2020-06-15T05:32:26Z",
                        "type":"None",
                        "priority":"None",
                        "status":"new",
                        "requester_id":398958715791,
                        "submitter_id":398958715791,
                        "assignee_id":"None",
                        "organization_id":"None",
                        "group_id":360005899611,
                        "brand_id":360002831091,
                        "form_id":360000514592,
                        "external_id":"None",
                        "tags":[

                        ],
                        "via":{
                          "channel":"web"
                        }
                    }
                  }
              }
            }
      if event_type == 'unsupported_file_type_attached':
          return {
              "version":"0",
              "id":"7e784552-fceb-eb6c-5598-cf0a301a64a7",
              "detail-type":"Support Ticket: Attachment Linked to Comment",
              "source":"aws.partner/zendesk.com/1234/default",
              "account":"426339633214",
              "time":"2020-06-15T05:32:28Z",
              "region":"us-west-2",
              "resources":[
                  "Support Ticket"
              ],
              "detail":{
                  "ticket_event":{
                    "meta":{
                        "version":"1.0",
                        "occurred_at":"2020-06-15T05:32:26Z",
                        "ref":"21-461478505",
                        "sequence":{
                          "id":"99246BC29B2E62BDA0DD85CF17977BB9",
                          "position":1,
                          "total":2
                        }
                    },
                    "type":"Attachment Linked to Comment",
                    "attachment":{
                        "id":376856773391,
                        "content_url":"https://subdomain.zendesk.com/attachments/token/1234/?name=sheet.xlsx",
                        "content_type":"xlsx",
                        "filename":"sheet.xlsx",
                        "is_public":True,
                        "comment_id":1088758661652
                    },
                    "ticket":{
                        "id":53,
                        "created_at":"2020-06-14T19:20:39Z",
                        "updated_at":"2020-06-15T05:32:26Z",
                        "type":"None",
                        "priority":"None",
                        "status":"new",
                        "requester_id":398958715791,
                        "submitter_id":398958715791,
                        "assignee_id":"None",
                        "organization_id":"None",
                        "group_id":360005899611,
                        "brand_id":360002831091,
                        "form_id":360000514592,
                        "external_id":"None",
                        "tags":[

                        ],
                        "via":{
                          "channel":"web"
                        }
                    }
                  }
              }
            }

if __name__ == '__main__':
    unittest.main()