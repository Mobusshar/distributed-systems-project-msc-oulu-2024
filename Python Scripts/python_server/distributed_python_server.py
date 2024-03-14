# Command to run the server: uvicorn distributed_python_server:app --reload
from fastapi import FastAPI,Depends, HTTPException, status
from pydantic import BaseModel
import pika
import json
import socket
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import mysql.connector
import bcrypt
import pyodbc


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "C8FrHTtnlGYFTzJoW_avnnFi3SeRm5vr_97qEsLVTLg"
ALGORITHM = "HS256"
app = FastAPI()

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def connect_to_database():
    server ="MTalhaArshad"
    database ="Messages"
    username ="test2"
    password  ="test2"
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trust_Connection=yes;'
    conn = pyodbc.connect(conn_str)
    print("Connected to the database")
    return conn

def verify_password(plain_password, hashed_password):
    # Verify the entered password against the hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
class DataInput(BaseModel):
    user_Id: str
    request_url: str
    type: int

# Pydantic model for user data
class User(BaseModel):
    email: str
    password: str

def authenticate_user(email: str, password: str):
    db_connection = connect_to_database()
    db_cursor = db_connection.cursor()
    # db_cursor.execute("SELECT email, password FROM users WHERE email = %s", (email,))
    db_cursor.execute("SELECT email, hashedpassword FROM users WHERE email = 'fgh'", ())

    user = db_cursor.fetchone()
    db_cursor.close()
    db_connection.close()
    if not user:
        return False
    if not verify_password(password, user[1]):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = authenticate_user(form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    user = ['ahmedzahid@oulu.fi']
    access_token = create_access_token({"sub": user[0]})
    return {"access_token": access_token, "token_type": "bearer"}

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


@app.post("/users/")
async def create_user(user: User):
    # return {"message": "User created successfully"}
    # Connect to the database
    db_connection = connect_to_database()
    db_cursor = db_connection.cursor()

    try:
        print("Hwew")
        print(user.email)
        print(user.password)
        # Check if the email is already registered
        # db_cursor.execute("SELECT email FROM users WHERE email = %s", (user.email,))
        db_cursor.execute("SELECT email FROM users WHERE email=(?)", (user.email))

        existing_user = db_cursor.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the password
        my_hashed_password = hash_password(user.password)

        # Insert the user into the database
        insert_query = "INSERT INTO users (email, hashedpassword) VALUES (?, ?)"
        user_data = (user.email, my_hashed_password)
        db_cursor.execute(insert_query, user_data)
        db_connection.commit()
        return {"message": "User created successfully"}

    finally:
        # Close cursor and connection
        db_cursor.close()
        db_connection.close()

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