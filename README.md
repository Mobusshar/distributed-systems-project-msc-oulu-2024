![GitHub commit activity](https://img.shields.io/github/commit-activity/t/mobusshar/distributed-systems-project-msc-oulu-2024)
![GitHub last commit](https://img.shields.io/github/last-commit/mobusshar/distributed-systems-project-msc-oulu-2024)
![GitHub top language](https://img.shields.io/github/languages/top/mobusshar/distributed-systems-project-msc-oulu-2024)
![GitHub language count](https://img.shields.io/github/languages/count/mobusshar/distributed-systems-project-msc-oulu-2024)
![GitHub License](https://img.shields.io/github/license/mobusshar/distributed-systems-project-msc-oulu-2024)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/mobusshar/distributed-systems-project-msc-oulu-2024)
![GitHub repo size](https://img.shields.io/github/repo-size/mobusshar/distributed-systems-project-msc-oulu-2024)
![GitHub forks](https://img.shields.io/github/forks/mobusshar/distributed-systems-project-msc-oulu-2024)
![GitHub Repo stars](https://img.shields.io/github/stars/mobusshar/distributed-systems-project-msc-oulu-2024)


![Alt text](https://github.com/Mobusshar/distributed-systems-project-msc-oulu-2024/blob/main/Images/systemDesign.jpg)




# Distributed Systems Course Project 2024 - Team Tesla

## Project Overview

This project is developed as part of the **Distributed Systems (521290S)** course and aims to process requests for scraping data from websites. The project involves the creation of a distributed system with various components like load balancers, message queuing systems, and fault-tolerant resource management.

The system's main objective is to handle high volumes of client requests in an efficient and scalable manner, implementing robust mechanisms for resource management and fault tolerance.

## Team Members

| Name                 | Student ID | Email                                  | Track     |
|----------------------|------------|----------------------------------------|-----------|
| Md Mobusshar Islam    | 2305578    | mislam23@student.oulu.fi               | Corporate |
| Muhammad Ahmed        | 2304796    | mahmed23@student.oulu.fi               | Corporate |
| Muhammad Talha Arshad | 2304797    | Muhammad.arshad@student.oulu.fi        | Corporate |

## System Architecture

The system is designed with an **Event-Driven Architecture (EDA)**. Nodes send requests to a load balancer, which distributes them across multiple servers using algorithms such as **Weighted Round Robin**. The backend infrastructure consists of Dockerized services, Nginx for load balancing, and RabbitMQ for message queuing.

**Key Components:**

- **Requesting Nodes:** Utility scripts generate mock requests.
- **Load Balancer:** Routes incoming requests using round-robin techniques.
- **Central Server:** Receives and queues messages for processing.
- **Message Broker (RabbitMQ):** Publishes requests to different consumers based on the request type.
- **Consumers:** Handle tasks like fetching website data, HTML, and domains.
- **Callback/Webhook:** Sends the response back to the client upon request completion.

## Implementation Details

### Client-Side Implementation:
- Python (Flask API) and C# (ASP.NET Core) for backend development.
- RESTful APIs for communication.

### Server-Side Implementation:
- Python and C# microservices.
- MSSQL for database interaction.
- PyODBC for Python, Entity Framework Core for C#.
- Docker for containerization, Nginx as a load balancer.

### Message Queuing System:
- RabbitMQ for handling and distributing messages.

### Fault Tolerance:
- Multiple servers handle requests using load balancing techniques (Weighted Round Robin).
- If a server goes down, requests are routed to the remaining live servers.
- RabbitMQ ensures that messages remain in the queue until processed.

## Communication

- **Pattern:** Publish/Subscribe
- **Protocol:** HTTP (via REST API)
- **Message Format:** JSON
- **Components:** Docker, MS SQL, RabbitMQ

## Security

- **User Registration:** Uses secure password hashing (SHA56) and stores user data in a MySQL database.
- **Authentication:** JWT-based authentication.
- **Authorization:** Token-based authorization for all API calls.

## Installation Instructions

### Prerequisites
1. Docker: [Install Docker](https://www.docker.com/)
2. Python 3.10: [Install Python](https://www.python.org/)
3. .NET Core 8.0 (C#10): [Install .NET Core](https://dotnet.microsoft.com/en-us/download)
4. RabbitMQ: [Install RabbitMQ](https://www.rabbitmq.com/)
5. MSSQL Server: [Install MSSQL Server](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
6. Nginx: [Install Nginx](https://www.nginx.com/)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mobusshar/distributed-systems-project-msc-oulu-2024.git
   ```
2. **Run Python Scripts**
   ```bash
   docker compose up --build
   ```
3. **MSSQL Setup**
   ```bash
       USE [Messages]
      CREATE TABLE [dbo].[Messages] (
        [Id] INT IDENTITY(1,1) NOT NULL,
        [user_Id] NVARCHAR(100),
        [request_url] NVARCHAR(100),
        [type] INT,
        [Is_processed] BIT DEFAULT 0,
        [callback_url] NVARCHAR(100),
        [date_added] DATETIME DEFAULT GETDATE(),
        [date_process_complete] DATETIME,
        [Is_processing] BIT DEFAULT 0,
        PRIMARY KEY CLUSTERED ([Id] ASC)
      )
   ```
4. ### C# Setup

1. **Message Storage:**
   - Use the `MessageBroker_1_RequestRecording` solution to store incoming requests in the MSSQL database. This solution captures and records all requests from the system to ensure they are properly logged into the `Messages` table.

2. **Publishing Requests:**
   - Run the `PublisherFromDB` solution to publish the stored requests from the MSSQL database. This solution reads the requests from the database and sends them to RabbitMQ for processing.

3. **Processing Requests:**
   - Use the `RabbitMQConsumer` solution to process the published requests. This solution subscribes to the RabbitMQ queues and handles the actual request processing, sending callbacks to the respective clients once the request is completed.

## Testing and Evaluation

### Load Balancing Techniques:
The system has been evaluated using the following load balancing techniques:

1. **Round Robin:** 
   - Requests are distributed evenly across the servers in a circular manner.

2. **Weighted Round Robin:** 
   - Servers are assigned different weights, allowing more powerful servers to handle a larger portion of the requests.

3. **Least Connection:** 
   - Requests are routed to the server with the fewest active connections to balance the load more efficiently.

### Fault Tolerance:
The system has been tested for fault tolerance using the following simulations:

1. **Server Down Simulation:**
   - A server is intentionally taken offline to observe how the system reroutes requests to the remaining live servers without interrupting the service.

2. **Queue System Shutdown Simulation:**
   - The RabbitMQ queue system is temporarily shut down to test how the system manages pending requests and processes them once the queue system is restored.

## License

This project is distributed under the MIT License.


