# command to run the client
import requests
import random
# It is just a UUID which the user was assigned when the user logged in.
# Consider the UUID as a unique key in our database for the user.
import uuid
from concurrent.futures import ThreadPoolExecutor

# ----------Creating a User   -------------- #
base_url = "http://localhost:8000"
# user_data = {"email": "example2@example.com", "password": "examplepassword"}
# create_user_response = requests.post(f"{base_url}/users/", json=user_data)
# print("Create User Response:", create_user_response.json())

# -------------- Creating JWT for a user --------------- #
# token_data = {"username": "example2@example.com", "password": "examplepassword"}
# token_response = requests.post(f"{base_url}/token", data=token_data)
# token = token_response.json()["access_token"]
# print("JWT Token:", token)
# quit()
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhaG1lZHphaGlkQG91bHUuZmkifQ.6nQHvbOQYQhgqQR23W5yWVrLPETEtKUPLUgh1Mh8BGM'
# protected_endpoint_response = requests.post(
#     f"{base_url}/receive_data",
#     headers={"Authorization": f"Bearer {token}"},
#     json={"user_id": "123", "request_url": "example.com", "type": 1}
# ).json()
# print(protected_endpoint_response)

# quit()

def send_request(url, user_id, request_url, type):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhaG1lZHphaGlkQG91bHUuZmkifQ.6nQHvbOQYQhgqQR23W5yWVrLPETEtKUPLUgh1Mh8BGM'
    data = {"user_Id": user_id, "request_url": request_url, "type": type}
    response = requests.post(url, json=data,headers={"Authorization": f"Bearer {token}"})
    result = response.json()
    print(result)  # Print result immediately after getting response
    return result


base_url = "http://127.0.0.1:8000/receive_data"
request_urls = [
    "https://www.varma.fi/en/self-employed/yel-insurance/determination-of-yel-income/",
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
    "https://example.com/page4"
]

# Generate unique user IDs for each request
user_ids = [str(uuid.uuid4()) for _ in range(5)]

# Use ThreadPoolExecutor to send requests in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    # Submit each request to the executor
    futures = [
        executor.submit(send_request, base_url, user_id, request_url, random.randint(1, 3))
        for user_id, request_url in zip(user_ids, request_urls)
    ]

    # Note: No need to wait for all requests to be processed
