using Payment.FieldList;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

/****************************************************
 * @File: IPayment.cs                               *
 * @Author: Questi0nM4rk                            *
 * @Date: 01/19/2023                                *
 *                                                  *
 * @copyright Copyright (c) 2023 Questi0nM4rk       *
 ****************************************************/

namespace Payment
{
    [Guid("9b9e4e80-c404-442b-83a9-3ada73b76fc7")]
    [InterfaceType(ComInterfaceType.InterfaceIsDual)]
    public interface IPayment
    {
        bool Sale(string Amount, string CurrencyCode, string VariableSymbol, out string response, out string err);
        bool Refund(string Amount, string CurrencyCode, string VariableSymbol, out string response, out string err);
        bool ReprintReciept(out string response, out string err);
        bool HandShake(out string response, out string err);
        bool SetIPnPORT(string ip, int port);
        bool Disconnect();
        bool Reconnect(out string err);
    }
}
