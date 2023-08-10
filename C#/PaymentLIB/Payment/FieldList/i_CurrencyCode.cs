using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class i_CurrencyCode : FieldListBase
    {
        public static string Content { get; set; }
        public i_CurrencyCode(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("CurrencyCode - parameters");
        }

        public static bool Validate()
        {

            switch (Content)
            {
                case "203":                         //CZK
                    Content = Data.Curr_code.CZK;
                    break;
                case "978":                         //EUR
                    Content = Data.Curr_code.EUR;
                    break;
                case "840":                         //USD
                    Content = Data.Curr_code.USD;
                    break;
                case "826":                         //GBP
                    Content = Data.Curr_code.GBP;
                    break;
                case "643":                         //RUB
                    Content = Data.Curr_code.RUB;
                    break;
                case "946":                         //RON
                    Content = Data.Curr_code.RON;
                    break;
                case "348":                         //HUF
                    Content = Data.Curr_code.HUF;
                    break;
                default:
                    throw new Exception("Currency code isnt in Currency list");
            }

            return Validator("N", 2, 3, "CurrencyCode", Content);

        }

        
    }
}
