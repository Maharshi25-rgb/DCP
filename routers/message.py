from fastapi import APIRouter
from models.message import Message
from services.message_service import process_message

router = APIRouter()


@router.post("/message")
def receive_message(data: Message):
    result = process_message(data.message)

    return {
        "user_message": data.message,
        "result": result
    }