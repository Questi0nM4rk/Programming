using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class q_SequenceNum : FieldListBase
    {
        public static string Content { get; set; }

        public q_SequenceNum(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("SequenceNum - parameters");
        }

        public static bool Validate()
        {
            return Validator("N", 1, 10, "SequenceNum", Content);

        }
    }
}
