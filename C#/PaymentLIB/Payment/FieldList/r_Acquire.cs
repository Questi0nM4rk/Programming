using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class r_Acquire : FieldListBase
    {
        public static string Content { get; set; }

        public r_Acquire(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("r_Acquire - parameters");
        }

        public static bool Validate()
        {
            return Validator("N", 2, 2, "r_Acquire", Content);

        }
    }
}
