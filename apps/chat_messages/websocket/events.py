from enum import StrEnum

class ChatEvent(StrEnum):
    SEND_MESSAGE = "SEND_MESSAGE"
    RECALL_MESSAGE = "RECALL_MESSAGE"