# Command to run the server: uvicorn callbacklogic:app --reload --port 8010
from fastapi import FastAPI
from pydantic import BaseModel


class DataInput(BaseModel):
    user_id: str
    status: str


app = FastAPI()


@app.post("/callback")
async def read_root(data: DataInput):
    response_object = {"success": True, "message": "callback received message"}
    print(f"Calling callback message:{data.dict()}")

    return response_object

# docker compose up --build
#  http://127.0.0.1:8000/callback
