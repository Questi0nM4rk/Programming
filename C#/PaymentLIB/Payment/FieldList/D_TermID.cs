﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Payment.FieldList
{
    public class D_TermID : FieldListBase
    {
        public static string Content { get; set; }
        public D_TermID(string par)
        {
            Content = par;
        }

        protected override string GetExecuteValue()
        {
            if (Validate()) return Content;
            else throw new Exception("TermID - parameters");
        }

        public static bool Validate()
        {
            return Validator("AN", 8, 18, "TermID", Content);
            
        }
    }
}
