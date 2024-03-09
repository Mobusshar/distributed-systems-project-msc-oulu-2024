# Command to run the server: uvicorn distributed_python_server:app --reload
from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json

class DataInput(BaseModel):
    user_id: str
    request_url: str
    type: int

def publish_to_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='data_queue')
    channel.basic_publish(exchange='', routing_key='data_queue', body=json.dumps(data))
    print(" [x] Sent message to queue")
    connection.close()

app = FastAPI()


@app.post("/receive_data")
async def read_root(data: DataInput):
    response_object = {"success": False, "data": {}, "message": "message received"}
    print(f"Incoming request client:{data}")
    response_object['success'] = True
    publish_to_queue(data.dict())
    return response_object

@app.get("/test_endpoint")
async def read_root():
    response_object = {"success": True, "data": {}, "message": "request received."}
    return response_object