using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class a_AuthorizationCode : FieldListBase
    {
        public static string Content { get; set; }

        public a_AuthorizationCode(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("AuthorizationCode - parameters");
        }

        public static bool Validate()
        {
            return Validator("AN", 1, 8, "AuthorizationCode", Content);

        }
    }
}
