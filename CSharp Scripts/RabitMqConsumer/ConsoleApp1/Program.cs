using System;
using System.Text;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;
using Newtonsoft.Json;
using System.Threading;
using System.Threading.Tasks;
using ConsoleApp1;


class Program
{
    static void Main(string[] args)
    {
        // Set up connection to RabbitMQ
        var factory = new ConnectionFactory() { HostName = "localhost" };
        using var connection = factory.CreateConnection();
        using var channel = connection.CreateModel();
        //using var dbContext = new AppDbContext();

        // Declare a direct exchange
        var exchangeName = "exchange";
        var exchangeType = "direct";

        channel.ExchangeDeclare(exchange: exchangeName, type: exchangeType);

        // Create queues for each message type
        for (int i = 1; i <= 3; i++)
        {
            var queueName = $"type_{i}_queue";
            channel.QueueDeclare(queue: queueName, durable: true, exclusive: false, autoDelete: false, arguments: null);

            channel.QueueBind(queue: queueName, exchange: exchangeName, routingKey: $"{i}_{exchangeName}");

            Task.Run(() => StartConsumer(channel, queueName));
        }

        Console.WriteLine("Press [enter] to exit.");
        Console.ReadLine();

    }


    static void StartConsumer(IModel channel, string queueName)
    {
        var consumer = new EventingBasicConsumer(channel);
        consumer.Received += async (model, ea) =>
        {
            var body = ea.Body.ToArray();
            var message = Encoding.UTF8.GetString(body);

            var messageData = JsonConvert.DeserializeObject<ApplicationDBContext.MessageData>(message);

            Console.WriteLine($"Started {queueName}");

            // Simulate processing time by sleeping for 5 seconds asynchronously
            await Task.Delay(GetProcessingTime(queueName));

            // Print the end task
            Console.WriteLine($"Finished {queueName}");

            SendCallBackRequest.SendPostRequest("http://127.0.0.1:8010/callback", messageData.user_Id, "Prcocess completed!");

            // Update database after processing
            //await UpdateDatabase(dbContext, messageData.Id);
        };

        channel.BasicConsume(queue: queueName, autoAck: true, consumer: consumer);
    }

  

    static int GetProcessingTime(string queueName)
    {
        return queueName switch
        {
            "type_1_queue" => 3000,
            "type_2_queue" => 2000,
            "type_3_queue" => 1000,
            _ => throw new ArgumentException("Invalid queue name"),
        };
    }



}
