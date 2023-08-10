using NLog;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class C_CardNum : FieldListBase
    {
        public static string Content { get; set; }
        public C_CardNum(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("CardNumber - parameters");
        }

        public static bool Validate()
        {
            try
            {
                return Validator("NS", 3, 19, "CardNumber", Content);
            }
            catch(Exception e)
            {
                Console.WriteLine(e.Message);
                return false;
            }
            
        }
    }
}
