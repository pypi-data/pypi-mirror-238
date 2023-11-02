from typing import Optional


class Message:
    MessageId: str
    ReceiptHandle: str
    MD5OfBody: str
    Body: str
    Attributes: {
        str: str
    }
    MD5OfMessageAttributes: str
    MessageAttributes: {
        str: str
    }


class ResponseMetadata:
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict
    RetryAttempts: int


# sqs response

class ResponseSendMessage:
    MD5OfMessageBody: str
    MessageId: str
    ResponseMetadata: ResponseMetadata

    def __init__(self, **kwargs):
        self.MD5OfMessageBody = kwargs["MD5OfMessageBody"]
        self.MessageId = kwargs["MessageId"]
        self.ResponseMetadata = kwargs["ResponseMetadata"]


class ResponseGetMessages:
    Messages: list[Message]

    def __init__(self, messages: list[Message]):
        self.Messages = messages


class ResponseDeleteMessages:
    ResponseMetadata: ResponseMetadata

    def __init__(self, **kwargs):
        self.ResponseMetadata = kwargs["ResponseMetadata"]


class Response:
    success: bool = False
    data: Optional[ResponseGetMessages or ResponseSendMessage or None]
    error: Optional[str]

    def __init__(self, **kwargs):
        if "success" in kwargs:
            self.success = kwargs["success"]

        if "data" in kwargs:
            self.data = kwargs["data"]

        if "error" in kwargs:
            self.error = kwargs["error"]
