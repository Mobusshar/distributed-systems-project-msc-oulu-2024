using System;
using RabbitMQ.Client;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        // Set up connection to RabbitMQ
        var factory = new ConnectionFactory() { HostName = "localhost" };
        using (var connection = factory.CreateConnection())
        using (var channel = connection.CreateModel())
        {
            // Declare a queue
            channel.QueueDeclare(queue: "message_queue",
                                 durable: true,
                                 exclusive: false,
                                 autoDelete: false,
                                 arguments: null);

            Console.WriteLine("Enter message to send (Press 'q' to quit):");

            // Read messages from console input and publish to the queue
            while (true)
            {
                string message = Console.ReadLine();

                if (message.ToLower() == "q")
                    break;

                var body = Encoding.UTF8.GetBytes(message);

                channel.BasicPublish(exchange: "",
                                     routingKey: "message_queue",
                                     basicProperties: null,
                                     body: body);

                Console.WriteLine("Message sent: {0}", message);
            }
        }
    }
}
