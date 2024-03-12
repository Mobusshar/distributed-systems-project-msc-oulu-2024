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

// Define your model for storing data in the database
public class MessageData
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }
    public string user_Id { get; set; }
    public string request_url { get; set; }
    public int type { get; set; }

    public bool Is_processed { get; set; }

    public bool Is_processing { get; set; }
}

// Define your DbContext using Entity Framework Core
public class AppDbContext : DbContext
{
    public DbSet<MessageData> Messages { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder options)
        => options.UseSqlServer("Server=MTALHAARSHAD;Database=Messages;Integrated Security=True;TrustServerCertificate=True;Encrypt=True;");
}

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

            // Bind each queue to the exchange with routing key including both type and exchange name
            channel.QueueBind(queue: queueName, exchange: exchangeName, routingKey: $"{i}_{exchangeName}");


            // Start consumers for each queue concurrently
            Task.Run(() => StartConsumer(channel, queueName));
        }

        Console.WriteLine("Press [enter] to exit.");
        Console.ReadLine();

    }


    static void StartConsumer(IModel channel, string queueName)
    {
        var dbContext = new AppDbContext();

        var consumer = new EventingBasicConsumer(channel);
        consumer.Received += async (model, ea) =>
        {
            var body = ea.Body.ToArray();
            var message = Encoding.UTF8.GetString(body);

            var messageData = JsonConvert.DeserializeObject<MessageData>(message);

            Console.WriteLine($"Started {queueName}");

            // Simulate processing time by sleeping for 5 seconds asynchronously
            await Task.Delay(GetProcessingTime(queueName));

            // Print the end task
            Console.WriteLine($"Finished {queueName}");

            // Update database after processing
            //await UpdateDatabase(dbContext, messageData.Id);
        };

        channel.BasicConsume(queue: queueName, autoAck: true, consumer: consumer);
    }

    static async Task UpdateDatabase(AppDbContext dbContext, int messageId)
    {
        var message = await dbContext.Messages.FindAsync(messageId);
        if (message != null)
        {
            message.Is_processed = true;
            await dbContext.SaveChangesAsync();
        }
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
