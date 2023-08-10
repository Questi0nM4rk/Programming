using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class s_VariableSymbol : FieldListBase
    {
        public static string Content { get; set; }
        
        public s_VariableSymbol(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("VariableSymbol - parameters");
        }

        public static bool Validate()
        {
            return Validator("N", 1, 10, "VariableSymbol", Content);

        }
    }
}
