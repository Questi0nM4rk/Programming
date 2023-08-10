using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class d_TransCount : FieldListBase
    {
        public static string Content { get; set; }
        public d_TransCount(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("TransCount - parameters");
        }

        public static bool Validate()
        {
            return Validator("N", 1, 9, "TransCount", Content);

        }
    }
}
