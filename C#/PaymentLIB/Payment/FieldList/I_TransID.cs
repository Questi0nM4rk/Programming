using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class I_TransID : FieldListBase
    {
        public static string Content { get; set; }
        public I_TransID(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("TransID - parameters");
        }

        public static bool Validate()
        {
            return Validator("N", 1, 9, "TransID", Content);

        }
    }
}
