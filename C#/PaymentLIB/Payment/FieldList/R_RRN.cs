using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class R_RRN : FieldListBase
    {
        public static string Content { get; set; }

        public R_RRN(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("RRN - parameters");
        }

        public static bool Validate()
        {
            return Validator("AN", 1, 12, "RRN", Content);
        }
    }
}
