class SNSClientException(Exception):
    pass


class SQSClientTopicNotFound(SNSClientException):
    pass


class SQSClientPublishError(SNSClientException):
    pass
