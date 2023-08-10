using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.NetworkInformation;
using System.Runtime.ConstrainedExecution;
using System.Text;
using System.Threading.Tasks;

/****************************************************
 * @File: data.cs                                   *
 * @Author: Questi0nM4rk                            *
 * @Date: 01/19/2023                                *
 *                                                  *
 * @copyright Copyright (c) 2023 Questi0nM4rk       *
 ****************************************************/

namespace Payment
{
    internal class Data
    {
        public enum Header_MSGtype : int
        {
            Request = 1,
            Response = 2,
            Information_Response,
            Device_Request,
            Device_Response,
            Error_Response,
            Keep_alive_Request

        }

        public enum Data_MSGtype : int
        {
            Request = 0,
            Response = 5,
        }

        public enum ConChar : byte
        {
            STX = 0x02,                             // <STX> (Start of Text) - 0x02 - 2
            ETX = 0x03,                             // <ETX> (End of transmission text) - 0x03 - 3
            EOT = 0x04,                             // <EOT> (End of transmission) - 0x04 - 4
            ENQ = 0x05,                             // <ENQ> (Enquiry) - 0x05 - 5
            ACK = 0x06,                             // <ACK> (Acknowledgement) - 0x06 - 6
            NAK = 0x15,                             // <NAK> (Negative acknowledgement) - 0x15 - 21
            DLE = 0x10,
            WACK = 0x13,
            FS = 0x1c,                              // <FS> (Field Separator) - 0x1c - 28
            GS = 0x1d                               // <GS> (Group Separator) - 0x1d - 29
        }

        public enum Reference_number
        {
            E_NONE = 0,
            E_REFNUM_A = 'A',                       // A(0x41) - Follow Preauthorization
            E_REFNUM_B = 'B',                       // B(0x42) - Follow Balance McDonald
            E_REFNUM_C = 'C',                       // C(0x43) - Follow Complete Preauthorization
            E_REFNUM_D = 'D',                       // D(0x44) - Follow Recharge McDonald
            E_REFNUM_E = 'E',                       // E(0x45) - Follow eVoucher McDonald
            E_REFNUM_F = 'F',                       // F(0x46) - Follow Available Funds
            E_REFNUM_H = 'H',                       // H(0x48) - Follow Hash
            E_REFNUM_K = 'K',                       // K(0x4B) - Follow Key checksum
            E_REFNUM_P = 'P',                       // P(0x50) - Follow Sale,StoreValueInCard
            E_REFNUM_R = 'R',                       // R(0x52) - Follow Refund
            E_REFNUM_S = 'S',                       // S(0x53) - Follow nothing(Only SwipeCard)
            E_REFNUM_X = 'X',						// X(0x58) - Follow Reversal
        }

        public enum E_LanguageCode
        {
            E_LANGCODE_NONE = 0,                    // 0 - None
            E_LANGCODE_CS,                          // 1 - czech
            E_LANGCODE_EN,                          // 2 - english
            E_LANGCODE_DE,                          // 3 - german
            E_LANGCODE_SK,                          // 4 - slovak
            E_LANGCODE_ES,                          // 5 - spanish
            E_LANGCODE_FR,                          // 6 - french
            E_LANGCODE_HU,                          // 7 - hungarian
            E_LANGCODE_IT,                          // 8 - italian
            E_LANGCODE_RO,                          // 9 - romanian
        }

        public class DeviceID
        {
            public static string SourceDev = "90";
            public static string DestinationDev = "01";
        }

        public class TP_FlowFlag
        {
            public static string Nothing = "00";
            public static string Print_receipt = "01";
            public static string Offline_transaction = "02";
            public static string Hash_PAN = "04";
        }

        public class TransID
        {
            public static string Initialization = "02";
            public static string Restart = "04";
            public static string Handshake = "06";
            public static string Basic_terminal_settings = "07";
            public static string Status_Information = "20";
            public static string Settlement = "21";
            public static string Service_Function = "26";
            public static string Subtotals = "28";
            public static string Set_Language = "30";
            public static string Clear_Journal = "40";
            public static string Reprint_Reciept = "42";
            public static string Repeat_Last_Message = "43";
            public static string Card_Swipe = "75";
            public static string Card_Service = "76";
            public static string Card_Abort = "77";
        }

        public static class Curr_code
        {
            public static string Terminal_defaults = "00";
            public static string CZK = "01";                        //203
            public static string EUR = "02";                        //978
            public static string USD = "03";                        //840
            public static string GBP = "04";                        //826
            public static string RUB = "05";                        //643
            public static string RON = "06";                        //946
            public static string HUF = "07";                        //348
        }

        public static bool CheckAnswer(string code, out string message)
        {
            message = String.Empty;
            switch (code)
            {
                case "00":
                    message = "Transaction successful";
                    return true;
                case "01":
                    message = "Transaction failed";
                    return false;
                case "02":
                    message = "Device is busy";
                    return false;
                case "03":
                    message = "Incorrect acquirer";
                    return false;
                case "04":
                    message = "Unknown transaction";
                    return false;
                case "05":
                    message = "Partially succeeded";
                    return false;
                case "06":
                    message = "Device request error";
                    return false;
                case "07":
                    message = "Transaction aborted";
                    return false;
                case "09":
                    message = "Uncompleted pre-authorizations in batch. Settlement not performed.";
                    return false;
                case "10":
                    message = "Batch is pending / memory is full";
                    return false;
                case "11":
                    message = "Almost full memory – less than 10 transactions left";
                    return true;
                case "12":
                    message = "Paper in the terminal printer ran out";
                    return false;
                case "19":
                    message = "User cancelled";
                    return false;
                case "20":
                    message = "Error reading card";
                    return false;
                case "21":
                    message = "Card not inserted";
                    return false;
                case "22":
                    message = "Unsupported card";
                    return false;
                case "23":
                    message = "Invalid card";
                    return false;
                case "24":
                    message = "Manual entry not allowed";
                    return false;
                case "25":
                    message = "Expired card";
                    return false;
                case "26":
                    message = "Pre-valid card";
                    return false;
                case "27":
                    message = "Invalid manual entry";
                    return false;
                case "28":
                    message = "Invalid country";
                    return false;
                case "29":
                    message = "Invalid phone number";
                    return false;
                case "30":
                    message = "Unknown phone operator";
                    return false;
                case "31":
                    message = "Invalid barcode length";
                    return false;
                case "32":
                    message = "Wrong currency";
                    return false;
                case "40":
                    message = "Init not allowed, settle first";
                    return false;
                case "50":
                    message = "Bad invoice number";
                    return false;
                case "51":
                    message = "Invalid amount";
                    return false;
                case "52":
                    message = "No batch totals";
                    return false;
                case "53":
                    message = "Invalid PIN";
                    return false;
                case "54":
                    message = "PIN limit exceeded";
                    return false;
                case "55":
                    message = "Change of amount is not allowed";
                    return false;
                case "56":
                    message = "Already voided";
                    return false;
                case "57":
                    message = "System number duplicity";
                    return false;
                case "58":
                    message = "System number missing";
                    return false;
                case "60":
                    message = "Amount too low for Cashback";
                    return false;
                case "61":
                    message = "Cashback not allowed";
                    return false;
                case "62":
                    message = "Maximum Cashback amount exceeded";
                    return false;
                case "63":
                    message = "Cashback amount too low";
                    return false;
                case "70":
                    message = "Void not allowed";
                    return false;
                case "71":
                    message = "No transaction to abort";
                    return false;
                case "72":
                    message = "PID doesn’t match";
                    return false;
                case "75":
                    message = "Card removed";
                    return false;
                case "80":
                    message = "Products not allowed";
                    return false;
                case "81":
                    message = "Unsupported SAM module";
                    return false;
                case "82":
                    message = "Financial transaction approved and EET transaction declined";
                    return true;
                default:
                    message = "Invalid code - code is not in documentation";
                    return false;
            }
        }
    }
}
