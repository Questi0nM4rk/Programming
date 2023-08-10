using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class A_AddAmount : FieldListBase
    {
        public static string Content { get; set; }

        public A_AddAmount(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("AddAmount - parameters");
        }

        public static bool Validate()
        {
            return Validator("N", 1, 10, "AddAmount", Content);
        }
    }
}
