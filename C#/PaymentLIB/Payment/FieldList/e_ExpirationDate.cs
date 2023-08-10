using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class e_ExpirationDate : FieldListBase
    {
        public static string Content { get; set; }

        public e_ExpirationDate(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("ExpirationDate - parameters: needs to be MMYY");
        }

        public static bool Validate()
        {
            return Validator("N", 4, 4, "ExpirationDate", Content);

        }
    }
}
