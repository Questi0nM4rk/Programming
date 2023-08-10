using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class y_SpecificSymbol : FieldListBase
    {
        public static string Content { get; set; }

        public y_SpecificSymbol(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("SpecificSymbol - parameters");
        }

        public static bool Validate()
        {
            return Validator("N", 1, 10, "SpecificSymbol", Content);

        }
    }
}
