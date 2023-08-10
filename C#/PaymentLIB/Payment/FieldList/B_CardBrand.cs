using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class B_CardBrand : FieldListBase
    {
        public static string Content { get; set; }
        public B_CardBrand(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("CardBrand - parameters");
        }

        public static bool Validate()
        {
            try
            {
                var Cards = Terminal.SUPP_CARDS.Concat(Terminal.SUPP_M_CARDS).ToArray();

                if (!Cards.Contains(Content))
                {
                    throw new Exception($"Card isnt in the supported");
                }

                return Validator("AN", 1, 15, "CardBrand", Content);
            }
            catch(Exception e)
            {
                Console.WriteLine(e.Message);
                return false;
            }
        }
    }
}
