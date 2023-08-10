using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class H_CardHash : FieldListBase
    {
        public static string Content { get; set; }
        public H_CardHash(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("CardHash - parameters");
        }

        public static bool Validate()
        {
            try
            {
                if (Content[Content.Length - 5] != '=')
                {
                    throw new Exception("Card number and Expiry date must be separated by '=' ");
                }

                return Validator("AN", 40, 40, "CardHash", Content);
            }
            catch(Exception e)
            {
                Console.WriteLine(e.Message);
                return false;
            }

        }
    }
}
