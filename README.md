# eventbridge-integration-solution-zendesk-attachment-processing
## Amazon EventBridge Integration Solution for Zendesk Attachment Processing

This Quick Start demonstrates an integration with AWS Step Function and AWS Lambda for Amazon EventBridge SaaS Partner Zendesk. When an image or PDF attachment is added to a Zendesk ticket, this integration will process the attachment and then update the Zendesk ticket with text and images identified in the attachment. This solution enables your Amazon EventBridge event bus to trigger a rule that evaluates all events and invokes an AWS Step Functions state machine as a target for matched events (i.e., an attachment is added to a ticket). Once sent to Step Functions, Lambda functions are invoked that:

1. Extract values like attachment URL and ticket ID from the matched event and upload the attachment file to S3
2. In parallel, detects the image labels using Amazon Rekognition & detects text using Amazon Textract
3. Updates the Zendesk ticket with text and images identified via the Zendesk API

You can use this as a starter project to extend this solution for any scenario that can use Step Functions and Lambda to orchestrate and run code.

![Quick Start architecture for EventBridge Integration Solution for Zendesk Attachment Processing](https://github.com/aws-quickstart/eventbridge-integration-solution-zendesk-attachment-processing/raw/master/images/arch-zendesk-attachments.png)

To post feedback, submit feature ideas, or report bugs, use the **Issues** section of [this GitHub repo](https://github.com/aws-quickstart/eventbridge-integration-solution-zendesk-attachment-processing).

