from enum import Enum

class MessageResponse(Enum):
    SUCCESS = "Ok"
    ERROR = "Error"
    MESSAGE_CREATED = "Created"
    MESSAGE_UNAUTHORIZED = "Unauthorized"
    MESSAGE_NOTFOUND = "Not Found"
    MESSAGE_INTERNAL = "Internal Server Error"
    MESSAGE_BAD_GATEWAY = "Bad Gateway"
    MESSAGE_FOUND = "Found register"
