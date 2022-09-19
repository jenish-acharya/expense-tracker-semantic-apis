import random

import spacy
from fastapi import FastAPI
from pydantic import BaseModel

import semanticsms


class Message(BaseModel):
    message_body: str


app = FastAPI()
nlp = spacy.load('en_core_web_sm')

@app.post("/analyse_sms/")
async def analyse_sms(message: Message):
    message_body = message.message_body
    message_doc = nlp(message_body)
    extracted_amount = semanticsms.extract_amount(message_doc)
    message_type = ["debit", "credit"]    
    data = {
        "extracted_amount": extracted_amount,
        "message_type": random.choice(message_type)
    }
    return data
