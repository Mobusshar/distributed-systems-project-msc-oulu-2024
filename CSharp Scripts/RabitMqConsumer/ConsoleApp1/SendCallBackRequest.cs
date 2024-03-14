using Microsoft.EntityFrameworkCore;
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using ConsoleApp1;

public class SendCallBackRequest
{
    private static readonly HttpClient client = new HttpClient();

    public static async Task SendPostRequest(string url, string userId, string status)
    {
        try
        {
            var postData = new
            {
                user_id = userId,
                status = status
            };
            var jsonContent = new StringContent(Newtonsoft.Json.JsonConvert.SerializeObject(postData), Encoding.UTF8, "application/json");

            HttpResponseMessage response = await client.PostAsync(url, jsonContent);

            if (response.IsSuccessStatusCode)
            {
                using (var dbContext = new ApplicationDBContext.AppDbContext())
                {
                    var message = dbContext.Messages.ToList();
                     message.Where(p => p.user_Id == userId).FirstOrDefault().Is_processed = true;
                     dbContext.SaveChanges();
                }

                Console.WriteLine("POST request sent successfully.");
            }
            else
            {
                Console.WriteLine($"Failed to send POST request. Status code: {response.StatusCode}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
    }
}