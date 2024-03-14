# command to run the client
import requests
import random
# It is just a UUID which the user was assigned when the user logged in.
# Consider the UUID as a unique key in our database for the user.
import uuid
from concurrent.futures import ThreadPoolExecutor


def send_request(url, user_id, request_url, type):
    data = {"user_Id": user_id, "request_url": request_url, "type": type}
    response = requests.post(url, json=data)
    result = response.json()
    print(result)  # Print result immediately after getting response
    return result


base_url = "http://127.0.0.1:8005/receive_data"
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
