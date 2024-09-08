from fastapi import FastAPI
from pydantic import BaseModel
import chatbot
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Message(BaseModel) :
    message : str 


@app.get('/')
async def status():
    return { "status" : 200  }


@app.post('/message')
async def status(message : Message="None"):
    if message != "None":
        
        return {"answer" : chatbot.process_answer(message.message)}
    else :
        return {"message" : "Cant Answer !"}