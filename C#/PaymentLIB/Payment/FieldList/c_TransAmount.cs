using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class c_TransAmount : FieldListBase
    {
        public static string Content { get; set; }
        public c_TransAmount(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("TransAmount - parameters");
        }

        public static bool Validate()
        {
            return Validator("N", 1, 12, "TransAmount", Content);

        }
    }
}
