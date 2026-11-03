from rest_framework.exceptions import APIException
from rest_framework import status

class TaskLimitExceeded(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Project task limit reached. You cannot add more than 10 tasks.'
    default_code = 'task_limit_exceeded'

class InvalidTaskAction(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This action is not allowed.'
    default_code = 'invalid_task_action'