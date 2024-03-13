# Command to run the server: uvicorn distributed_python_server:app --reload
from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json
import socket


class DataInput(BaseModel):
    user_Id: str
    request_url: str
    type: int


def publish_to_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('host.docker.internal'))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_exchange', exchange_type='direct')
    channel.queue_declare(queue='data_queue', durable=True)
    channel.queue_bind(exchange='direct_exchange', queue='data_queue', routing_key=str(data['type']))
    channel.basic_publish(exchange='direct_exchange', routing_key=str(data['type']), body=json.dumps(data))
    print(" [x] Sent message to queue")
    connection.close()



# def publish_to_queue(data):
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
#     channel = connection.channel()
#     channel.queue_declare(queue='data_queue')
#     channel.basic_publish(exchange='', routing_key='data_queue', body=json.dumps(data))
#     print(" [x] Sent message to queue")
#     connection.close()

app = FastAPI()


@app.post("/receive_data")
async def read_root(data: DataInput):
    response_object = {"success": False, "data": {"id": socket.gethostname()}, "message": "message received"}
    print(f"Incoming request client:{data}")
    response_object['success'] = True
    publish_to_queue(data.dict())
    return response_object


# We have used Nginx for our system to implement the load balancing technique.
@app.get("/test_endpoint")
async def read_root():
    response_object = {"success": True, "data": {"id": socket.gethostname()}, "message": "request received."}
    return response_object


# docker compose up --build
# https://www.nginx.com/resources/wiki/start/topics/examples/full/