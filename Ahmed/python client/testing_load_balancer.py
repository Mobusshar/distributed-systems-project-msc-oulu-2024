import requests
import uuid

MAX_REQUESTS = 100

data = {}

# for i in range(100):
#     res = requests.get("http://localhost:8000/test_endpoint")
#     # print(res)
#     id = res.json()['data']["id"]
#     if data.get(id):
#         data[id] = data[id] + 1
#     else:
#         data[id] = 1
#
# print(data)
# quit()

domains = [
    "varma.fi",
    "example.com",
    "example1.com",
    "example2.com",
    "example3.com",
    "example4.com",
    "example5.com",
    "example6.com",
    "example7.com",
    "example8.com",
    "example9.com",
    "example0.com",
    "varma1.fi",
    "varma2.fi",
    "varma3.fi",
    "varma4.fi",
    "varma5.fi",
    "varma6.fi",
    "varma7.fi",
    "varma8.fi",
    "varma9.fi",
    "varma0.fi",
    "ex1.com",
    "ex2.com",
    "ex3.com",
    "ex4.com",
    "ex5.com",
    "ex6.com",
    "ex7.com",
    "ex8.com",
    "ex9.com",
    "ex0.com",
    "examplefi.com",
    "example1fi.com",
    "example2fi.com",
    "example3fi.com",
    "example4fi.com",
    "example5fi.com",
    "example6fi.com",
    "example7fi.com",
    "example8fi.com",
    "example9fi.com",
    "example0fi.com",
    "varmacom.fi",
    "varma1com.fi",
    "varma2com.fi",
    "varma3com.fi",
    "varma4com.fi",
    "varma5com.fi",
    "varma6com.fi",
    "varma7com.fi",
    "varma8com.fi",
    "varma9com.fi",
    "varma0com.fi",
    "varma1example.fi",
    "varma2example.fi",
    "varma3example.fi",
    "varma4example.fi",
    "varma5example.fi",
    "varma6example.fi",
    "varma7example.fi",
    "varma8example.fi",
    "varma9example.fi",
    "varma0example.fi",
    "example-com.fi",
    "example1-com.fi",
    "example2-com.fi",
    "example3-com.fi",
    "example4-com.fi",
    "example5-com.fi",
    "example6-com.fi",
    "example7-com.fi",
    "example8-com.fi",
    "example9-com.fi",
    "example0-com.fi",
    "example1examplecom.fi",
    "example2examplecom.fi",
    "example3examplecom.fi",
    "example4examplecom.fi",
    "example5examplecom.fi",
    "example6examplecom.fi",
    "example7examplecom.fi",
    "example8examplecom.fi",
    "example9examplecom.fi",
    "example0examplecom.fi",
    "example1com.fi",
    "example2com.fi",
    "example3com.fi",
    "example4com.fi",
    "example5com.fi",
    "example6com.fi",
    "example7com.fi",
    "example8com.fi",
    "example9com.fi",
    "example0com.fi",
    "example1example.fi",
    "example2example.fi",
    "example3example.fi",
    "example4example.fi",
    "example5example.fi"
]


def send_request(url, user_id, request_url, type):
    data = {"user_Id": user_id, "request_url": request_url, "type": type}
    response = requests.post(url, json=data)
    result = response.json()
    print(result)  # Print result immediately after getting response
    return result


for i in range(100):
    result = send_request("http://127.0.0.1:8000/receive_data",domains[i], str(uuid.uuid4()), 1)
    id = result['data']["id"]
    if data.get(id):
        data[id] = data[id] + 1
    else:
        data[id] = 1

print(data)
