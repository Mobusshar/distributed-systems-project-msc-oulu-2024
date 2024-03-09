using System;
using System.Text;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;
using Newtonsoft.Json;

// Define your model for storing data in the database
public class MessageData
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }
    public string user_uuid { get; set; }
    public string request_uuid { get; set; }
    public int type { get; set; }
    public string is_processed { get; set; }
}

// Define your DbContext using Entity Framework Core
public class AppDbContext : DbContext
{
    public DbSet<MessageData> Messages { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder options)
        => options.UseSqlServer("Server=MTALHAARSHAD;Database=PWPProject;Integrated Security=True;TrustServerCertificate=True;Encrypt=True;");
}

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

            // Create consumer to receive messages from the queue
            var consumer = new EventingBasicConsumer(channel);
            consumer.Received += (model, ea) =>
            {
                var body = ea.Body.ToArray();
                var message = Encoding.UTF8.GetString(body);
                Console.WriteLine("Received message: {0}", message);

                var messageData = JsonConvert.DeserializeObject<MessageData>(message);
                
                using (var dbContext = new AppDbContext())
                {
                    dbContext.Messages.Add(messageData);
                    dbContext.SaveChanges();
                }
            };

            // Start consuming messages from the queue
            channel.BasicConsume(queue: "message_queue",
                                 autoAck: true,
                                 consumer: consumer);

            Console.WriteLine("Press [enter] to exit.");
            Console.ReadLine();
        }
    }
}
