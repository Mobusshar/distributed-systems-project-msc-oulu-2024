using System;
using RabbitMQ.Client;
using System.Text;
using Newtonsoft.Json;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

public class MessageData
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public string user_Id { get; set; }
    public string request_url { get; set; }
    public int type { get; set; }
    public bool Is_processed { get; set; }
    //public bool Is_processing { get; set; }

    //public string callback_url { get; set; }
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
    static async Task Main(string[] args)
    {
        var factory = new ConnectionFactory() { HostName = "localhost" };
        using (var connection = factory.CreateConnection())
        using (var channel = connection.CreateModel())
        {
            var exchange1 = "exchange";
            var exchanges = new List<string> { exchange1};

            // Declare the exchanges
            foreach (var exchange in exchanges)
            {
                channel.ExchangeDeclare(exchange: exchange, type: ExchangeType.Direct);
            }
            var currentIndex = 0;


            while (true)
            {
                using (var dbContext = new AppDbContext())
                {
                    var messages = dbContext.Messages.Where(p => p.Is_processed == false).ToList();
                    foreach (var data in messages)
                    {
                        var messageData = new MessageData
                        {
                            user_Id = data.user_Id,
                            request_url = data.request_url,
                            type = data.type
                        };

                        var message = JsonConvert.SerializeObject(messageData);
                        var body = Encoding.UTF8.GetBytes(message);

                        var exchange = exchanges[currentIndex];
                        channel.BasicPublish(exchange: exchange,
                            routingKey: data.type + $"_{exchange}",
                            basicProperties: null,
                            body: body);

                        Console.WriteLine($"Message sent with type {data.type}.");

                        currentIndex = (currentIndex + 1) % exchanges.Count; // Round-robin index

                        data.Is_processed = true;
                        //dbContext.SaveChanges();
                    }
                }

                await Task.Delay(5000);
            }
        }
    }
}
