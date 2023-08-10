using Microsoft.SqlServer.Server;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class S_Amount : FieldListBase
    {
        public static string Content { get; set; }
        public S_Amount(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("Amount - parameters");
        }

        public static bool Validate()
        {
            if (Content.Contains(",") || Content.Contains("."))
            {
                string[] s = Content.Split(new char[] { ',', '.' });
                if (s[1].Length > 2) Array.Resize(ref s, 2);
                Content = String.Join("", s);
            }
            else Content = Content + "00";

            return Validator("N", 1, 10, "Amount", Content);

        }
    }
}
