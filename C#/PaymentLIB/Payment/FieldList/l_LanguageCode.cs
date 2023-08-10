using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class l_LanguageCode : FieldListBase
    {
        public static string Content { get; set; }

        public l_LanguageCode(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("LanguageCode - parameters");
        }

        public static bool Validate()
        {
            // map data from input to data.E_LanguageCode if language code will be used

            return Validator("N", 2, 2, "LanguageCode", Content);
        }
    }
}
