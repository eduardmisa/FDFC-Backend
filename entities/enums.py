from enum import Enum


class LogEnum(Enum):
    ADD = "Add"
    UPDATE = "Update"
    DELETED = "DELETED"

class LogEntitiesEnum(Enum):
    USR = "USR"

# MAKE SURE KEY IS EQUAL TO MODEL NAME
# e.g models.User >>> User
class PrefixEnum(Enum):
    User = "USR"
    FormState = "FRM"
