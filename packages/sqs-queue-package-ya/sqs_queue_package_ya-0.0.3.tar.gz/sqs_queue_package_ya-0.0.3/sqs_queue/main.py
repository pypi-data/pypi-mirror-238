import boto3
import os

from sqs_queue.interfaces import ResponseSendMessage, \
    ResponseGetMessages, Response, ResponseDeleteMessages


class SQSQueue:
    client = None
    queue_url = None

    def __init__(
            self,
            _endpoint_url: str,
            _queue_name: str,
            _aws_access_key_id: str,
            _aws_secret_access_key: str,
            _service_name: str,
            _region_name: str
    ):

        """
           Initializing a client to work with a queue

           Parameters
           ----------
           _endpoint_url: str
               queue url
           _queue_name: str
               queue name
           _aws_access_key_id: str
               aws access key id for sqs
           _aws_secret_access_key: str
               AWS secret key for sqs
           _service_name: str
               sqs
           _region_name: str
               queue region

           """
        try:
            os.environ['AWS_ACCESS_KEY_ID'] = _aws_access_key_id
            os.environ['AWS_SECRET_ACCESS_KEY'] = _aws_secret_access_key

            self.client = boto3.client(
                service_name=_service_name,
                endpoint_url=_endpoint_url,
                region_name=_region_name
            )

            self.queue_url = self.client.create_queue(
                QueueName=_queue_name
            ).get('QueueUrl')
        except BaseException as e:
            raise e

    def send_message(
            self,
            _queue_msg: str
    ) -> Response:
        """
           Send message to queue

           Parameters
           ----------
           _queue_msg: str
               data to be sent to the queue

           Returns
           -------
           Response
               request response
           """
        response = Response()

        try:
            res = self.client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=_queue_msg,
            )

            response.data = ResponseSendMessage(**res)
            response.success = True
        except BaseException as e:
            response.error = str(e)

        return response

    def get_messages(
            self,
            _maximum_number_of_messages: int = 10,
            _visibility_timeout: int = 1200,
            _wait_time_seconds: int = 10
    ) -> Response:
        """
           Get messages from queue

           Parameters
           ----------
           _maximum_number_of_messages: int
               maximum number of messages in queue for a result
           _visibility_timeout: int
               visibility time in the message queue, s
           _wait_time_seconds: int
               waiting time before receiving messages

           Returns
           -------
           Response
               request response
           """
        response = Response()

        try:
            res = self.client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=_maximum_number_of_messages,
                VisibilityTimeout=_visibility_timeout,
                WaitTimeSeconds=_wait_time_seconds
            ).get('Messages')

            response.data = ResponseGetMessages(
                messages=res
            )
            response.success = True
        except BaseException as e:
            response.error = str(e)

        return response

    def delete_message(
            self,
            _recept: str
    ) -> Response:
        """
           Delete message from queue

           Parameters
           ----------
           _recept: str
               ReceiptHandle field for removing a message from the queue

           Returns
           -------
           Response
               request response
           """
        response = Response()

        try:
            res = self.client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=_recept
            )

            response.data = ResponseDeleteMessages(**res)
            response.success = True
        except BaseException as e:
            response.error = str(e)

        return response

    def delete_all_messages(
            self
    ) -> Response:
        """
           Delete all messages from queue

           Returns
           -------
           Response
               request response
           """
        response = Response()

        try:
            res = self.client.purge_queue(
                QueueUrl=self.queue_url
            )

            response.data = ResponseDeleteMessages(**res)
            response.success = True
        except BaseException as e:
            response.error = str(e)

        return response
