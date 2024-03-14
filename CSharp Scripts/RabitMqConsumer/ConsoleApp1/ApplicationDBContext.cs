using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    internal class ApplicationDBContext
    {
        // Define your model for storing data in the database
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

        public class AppDbContext : DbContext
        {
            public DbSet<MessageData> Messages { get; set; }

            protected override void OnConfiguring(DbContextOptionsBuilder options)
                => options.UseSqlServer("Server=MTALHAARSHAD;Database=Messages;Integrated Security=True;TrustServerCertificate=True;Encrypt=True;");
        }

    }
}
