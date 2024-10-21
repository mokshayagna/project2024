from fastapi import FastAPI  # Importing FastAPI to create the web application
from pydantic import BaseModel  # Importing BaseModel to define the data model for our API

app = FastAPI()  # Creating an instance of the FastAPI class

# Initial message stored in memory
message_store = {"message": "Hello, World!"}  # This dictionary stores the current message

# Model for POST request
class Message(BaseModel):  # Defining a data model for our POST request
    message: str  # The model has one field: message, which is a string

# API 1: Get the current message
@app.get("/get-message")  # This defines a GET endpoint called /get-message
def get_message():
    return {"message": message_store["message"]}  # It returns the message from the message_store dictionary

# API 2: Set a new message
@app.post("/set-message")  # This defines a POST endpoint called /set-message
def set_message(new_message: Message):  # It takes a Message object as input
    message_store["message"] = new_message.message  # Updates the message in message_store
    return {"message": "Message updated successfully!"}  # Confirms the update

# Swagger docs and ReDoc are available by default:
# Swagger: /docs
# ReDoc: /redoc
