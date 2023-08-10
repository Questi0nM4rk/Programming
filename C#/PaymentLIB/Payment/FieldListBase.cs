using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Payment;

/****************************************************
 * @File: FieldListBase.cs                          *
 * @Author: Questi0nM4rk                            *
 * @Date: 01/19/2023                                *
 *                                                  *
 * @copyright Copyright (c) 2023 Questi0nM4rk       *
 ****************************************************/

namespace Payment.FieldList
{
    public abstract class FieldListBase : IFieldList
    {
        public virtual string GetValue()
        {
            
            return GetExecuteValue();
        }
        protected abstract string GetExecuteValue();

        private static Dictionary<char, char[]> VAL = new Dictionary<char, char[]>()
        {
            {'A', "A a B b C c D d E e F f G g H h I i J j K k L l M m N n O o P p Q q R r S s T t U u V v W w X x Y y Z z".Replace(" ", "").ToArray()},
            {'N', "0 1 2 3 4 5 6 7 8 9".Replace(" ", "").ToArray()},
            {'S', @"\ | ! # $ % & / ( ) = ? » « @ £ § € { } . - ; ' < > _ , + : @ [ ] ~ ^".Replace(" ", "").ToArray()},
        };

        protected static bool Validator(string PAR, int FR, int TO, string ATT ,string CONTROL, char[] SPEC = null)
        {
            List<char> CONTROL_ARR = new List<char>();

            try
            {
                foreach (char ch in PAR)
                {
                    char[] t = VAL[ch];

                    CONTROL_ARR.AddRange(t);
                }

                if (SPEC != null)
                {
                    CONTROL_ARR.AddRange(SPEC);
                }

                if (CONTROL.Length < FR || CONTROL.Length > TO)
                {
                    throw new Exception($"Length of {ATT} is out of range, should be <{FR}, {TO}>, but it is {CONTROL.Length}");
                }

                foreach(char ch in CONTROL)
                {
                    if(!CONTROL_ARR.Contains(ch))
                    {
                        throw new Exception($"Validation exeption of {ATT}. Only {PAR}(N-numeric|A-Alphabetical|S-Special) chars are allowed - '{ch}' is not allowed");
                    }
                }

                return true;
            }
            catch(Exception e)
            {
                throw new Exception(e.Message);
            }
        }
    }
}
