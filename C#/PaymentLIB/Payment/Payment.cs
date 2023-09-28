using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel;
using System.Data;
using System.IO.Ports;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using Payment.FieldList;
using System.IO;
using System.Runtime.InteropServices.ComTypes;
using System.Diagnostics;
using static Payment.Data;
using System.Runtime.InteropServices;

/****************************************************
 * @File: Terminal.cs - Main file of DLL            *
 * @Author: Questi0nM4rk                            *
 * @Date: 01/19/2023                                *
 *                                                  *
 * @copyright Copyright (c) 2023 Questi0nM4rk       *
 ****************************************************/

namespace Payment
{
    [Guid("bf62c79c-18ef-4592-9acb-7125ff2399f1")]
    [ClassInterface(ClassInterfaceType.None)]
    public class Terminal : IPayment
    {
        public string IP;
        public int PORT;

        // IP - ip of terminal (server)
        // ECR - ip of client

        private static string file = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\LOG.log";
        private static TcpClient tcpClient = new TcpClient();
        private static int TIMEOUT = 1_500; // 1,5s
        private static int NUM = 0;
        private static string MC = "";
        private static string SYSNUM = "";

        // atributes

        public static string[] SUPP_CARDS = { "VISA", "AMEX", "MC", "Maestro", "Diners", "JCB" };
        public static string[] SUPP_M_CARDS = { "AXA", "DOXX", "UP", "Callio", "Gusto", "EDENRED" };

        private static int x = 0; // num of tries - max 3


        //=============================================================================================================

        //---------------------------------- send message ----------------------------------

        /***************
         * @Documentation for msg_write
         * 
         * @msg_write function attempts to write the message to the given networkStream
         * 
        ****************/

        /// <summary>
        /// Attempts to write the contents of the byte array to the specified NetworkStream
        /// </summary>
        /// <param name="networkStream"></param>
        /// <param name="Msg"></param>
        /// <returns>True if passed</returns>
        /// <exception cref="Exception"></exception>

        private bool msg_write(NetworkStream networkStream, byte[] Msg)
        {
            try
            {
                networkStream.Write(Msg, 0, Msg.Length);
                Log($"{string.Join(" ", ToHex(ToMSG(Msg)))}", "S");
                //Console.WriteLine($"Message send: {string.Join(" ", ToHex(ToMSG(Msg)))}");
                return true;
            }
            catch (Exception e)
            {
                throw new Exception(e.Message);
            }
        }

        //---------------------------------- Write and Read message ----------------------------------

        /***************
         * @Documentation for WriteRead
         * 
         * @WriteRead function attempts to write and read the Message to the networkStream 3 times with 500ms timeout, it also converts the codes returned by terminal to text definition of each
         * 
        ****************/

        /// <summary>
        /// Attempts to write and read the Message to the networkStream 3 times with 500ms timeout, it also converts the codes returned by terminal to text definition of each
        /// </summary>
        /// <param name="networkStream"></param>
        /// <param name="Message"></param>
        /// <param name="code">The err and its definition returned by terminal</param>
        /// <returns>True if the transmission was succesful, else False and 98</returns>
        /// <exception cref="Exception"></exception>

        private bool WriteRead(NetworkStream networkStream, byte[] Message, out string code)
        {
            int attempts = 0;
            code = string.Empty;
            string code1 = string.Empty;
            bool passed = true;
            int y = 0;

            while (attempts < 3)
            {
                try
                {
                    tcpClient.ReceiveTimeout = 500;
                    byte[] data = Message;
                    byte[] checkByte = new byte[2];

                    // ------ Write ------
                    msg_write(networkStream, data);

                    // ------ Read ------
                    List<byte> l = new List<byte>();
                    List<byte> r = new List<byte>();

                    l = msg_read(networkStream).ToList();

                    if (l[0] == 6)
                    {
                        while (!networkStream.DataAvailable && y <= 150)
                        {
                            Thread.Sleep(500);
                            y++;
                        }

                        if (y >= 150)
                        {
                            code = "97:Terminal disconnected";
                            Log("97:Terminal disconnected", "E");
                            return false;
                        }

                        r = msg_read(networkStream).ToList();

                        if (r.Count < 1)
                        {
                            code = "97:Terminal not responding";
                            Log("97:Terminal not responding", "E");
                            return false;
                        }

                        else if (r.Count > 19)
                        {

                            string resp = string.Join("", ToMSG(r.ToArray()));
                            string[] splitted = resp.Split(new string[]{ "<FS>" }, StringSplitOptions.None);
                            //Console.WriteLine(string.Join("|", splitted));

                            //----------------------------------------------------
                            checkByte = new byte[] { r[20], r[21] };
                            code = String.Join("", ToMSG(checkByte)) + ":";

                            string card_num4 = "";
                            string id_uctenka = "";
                            string auth_code = "";
                            string tid = "";

                            if (splitted.Length > 30)
                            {
                                id_uctenka = splitted[39];
                                card_num4 = splitted[0];
                                card_num4 = card_num4.Substring(card_num4.IndexOf("******") + 6, 4);
                                auth_code = splitted[10].Split(' ')[1];
                                tid = splitted[3];
                            }

                            passed = CheckAnswer(String.Join("", ToMSG(checkByte)), out code1);
                            code += code1 + ":" + id_uctenka + ":" + card_num4 + ":" + tid + ":" + auth_code;
                        }
                        else
                        {
                            code = "X:Unknown message";
                            Log("X:Unknown message", "E");
                        }

                        Log(code, "M");
                    }
                    else if (l[0] == 21)
                    {
                        code = "98:Transaction declined by terminal";
                        Log("98:Transaction declined", "E");
                        return false;
                    }

                    return passed;

                }
                catch (SocketException e)
                {
                    if (e.SocketErrorCode == SocketError.TimedOut)
                    {
                        if (attempts >= 3)
                        {
                            tcpClient.Close();
                            Console.WriteLine("Failed to connect after 3 attempts. Disconnecting...");
                            Log("Failed to connect after 3 attempts. Disconnecting...", "E");
                            throw new Exception("Disconnecting...");
                        }
                        else
                        {
                            Console.WriteLine("Attempt {0} failed to connect. Timed out. Retrying...", attempts);
                            Log($"Attempt {attempts} failed to connect. Timed out. Retrying.", "W");
                            attempts++;
                        }
                    }
                    else
                    {
                        Console.WriteLine("Attempt {0} failed to connect. {1}", attempts, e.Message);
                        Log($"Attemp {attempts} faileed to connect. {e.Message}", "E");
                        throw new Exception("WriteRead:" + e.Message);
                    }
                }
            }
            return false;
        }

        //---------------------------------- message read ----------------------------------

        /***************
         * @Documentation for msg_read
         * 
         * @msg_read function attempts to read the response from the terminal on the given networkStream, 3 times with 500ms timeout
         * 
        ****************/

        /// <summary>
        /// Attempts to read the response from the terminal on the given networkStream, 3 times with 500ms timeout
        /// </summary>
        /// <param name="networkStream"></param>
        /// <returns>Byte representation of the response recived</returns>
        /// <exception cref="Exception"></exception>

        private byte[] msg_read(NetworkStream networkStream)
        {
            try
            {
                List<byte> l = new List<byte>();
                byte[] buffer = new byte[8];
                int y = 0;

                int bytesRead;
                MemoryStream ms = new MemoryStream();
                do
                {
                    bytesRead = networkStream.Read(buffer, 0, buffer.Length);
                    if (bytesRead > 0) ms.Write(buffer, 0, bytesRead);
                    y++;
                } while ((networkStream.DataAvailable && bytesRead > 0) && y < 100);

                l = ms.ToArray().ToList();

                //Console.WriteLine("Message recieved: {0}", string.Join(" ", ToHex(ToMSG(ms.ToArray()))));
                Console.WriteLine("\n=====\nMessage recieved: {0}", string.Join("", ToMSG(ms.ToArray())));
                Log($"{string.Join(" ", ToHex(ToMSG(ms.ToArray())))}", "R");

                return l.ToArray();
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                throw new Exception("Error while reading Message: " + e.Message);
            }
        }

        //---------------------------------- send Acknowledge ----------------------------------

        /***************
         * @Documentation for send_ACK
         * 
         * @send_ACK function is used to send <ACK> byte with the NUM variable that is used to connect send messages to the given networkStream which confirms the data recived and ens the transmission
         * 
        ****************/

        /// <summary>
        /// Sends the ACK byte to the given networkStream
        /// </summary>
        /// <param name="networkStream"></param>
        /// <returns>True if passed</returns>
        /// <exception cref="Exception"></exception>

        private bool send_ACK(NetworkStream networkStream)
        {
            try
            {
                byte ACK = (byte)ConChar.ACK;
                Console.WriteLine("Sending ACK");
                Log("ACK", "M");
                byte num = Convert.ToByte(Convert.ToString(NUM));
                msg_write(networkStream, new byte[] { ACK, num });
                return true;
            }

            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                throw new Exception("Error while sending ACK: " + e.Message);
            }
        }

        //---------------------------------- send Not Acknowledge ----------------------------------

        /***************
         * @Documentation for send_NAK
         * 
         * @send_NAK function is used to send <NAK> byte to the given networkStream which denies the data that was recived from the terminal
         * 
        ****************/

        /// <summary>
        /// Sends the NAK byte to the given networkStream
        /// </summary>
        /// <param name="networkStream"></param>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>

        private bool send_NAK(NetworkStream networkStream)
        {
            try
            {
                byte NAK = (byte)ConChar.NAK;
                Console.WriteLine("Sending NAK");
                Log("ACK", "M");
                msg_write(networkStream, new byte[] { NAK });
                msg_read(networkStream);
                return true;
            }

            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                throw new Exception("Error while sending NAK: " + e.Message);
            }
        }

        //---------------------------------- Set IP and PORT ----------------------------------

        /***************
         * @Documentation for SetIPnPORT
         * 
         * @SetIPnPORT function is used to set global variables for terminal IP and PORT
         * 
        ****************/

        /// <summary>
        /// Sets the IP and PORT for the terminal you wanna use in the session
        /// </summary>
        /// <param name="ip"></param>
        /// <param name="port"></param>
        /// <returns></returns>

        public bool SetIPnPORT(string ip, int port)
        {
            Log("IP and Port set", "M");
            PORT = port;
            IP = ip;
            return true;
        }

        //---------------------------------- Connect ----------------------------------

        /***************
         * @Documentation for Connect
         * 
         * @Connect attempts to connect to the global IP and PORT of the terminal given in SetIPnPORT function
         * 
        ****************/

        /// <summary>
        /// Attempts to connect to the IP and PORT given in SetIPnPORT up to 3 times with 1,5s timeout
        /// </summary>
        /// <param name="err"></param>
        /// <returns>True if connected and terminal response was ACK else returns False with err err</returns>
        private bool Connect(out string err)
        {
            try
            {
                if (x >= 3)
                {
                    Console.WriteLine("con_conn: The number of tries is more than 2.");
                    Log("Number of attempts reached", "E");
                    err = "99:Connection failed";
                    return false;
                }

                err = string.Empty;

                try { if (tcpClient.Connected) Disconnect(); } catch { tcpClient = new TcpClient(); }

                tcpClient = new TcpClient();

                tcpClient.ReceiveTimeout = TIMEOUT;
                tcpClient.SendTimeout = TIMEOUT;

                CancellationToken ct = new CancellationToken();
                if (!tcpClient.ConnectAsync(IPAddress.Parse(IP), PORT).Wait(TIMEOUT, ct))
                {
                    ct.ThrowIfCancellationRequested();
                    tcpClient.Close();

                    if (x < 3)
                    {
                        x++;
                        Console.WriteLine($"Socket_e: the connection timeouted... trying to reconect - attempts {x}/3");
                        Log($"Connection timedout, attempts {x}/3", "W");
                        Connect(out err);
                    }
                }

                NetworkStream networkStream = tcpClient.GetStream();
                Console.WriteLine($"con_conn: Socket connected to -> {IP}:{PORT} \nTesting connection...");
                List<string> read = ToMSG(msg_read(networkStream));

                Console.WriteLine("con_conn: " + string.Join("", read));

                if (read.Contains("<ENQ>"))
                {
                    x = 0;
                    Console.WriteLine("\ncon_conn: ETF connected");
                    Log("Connected", "M");
                    return true;
                }
                else
                {
                    err = "99:Connection failed";
                    Console.WriteLine("\ncon_conn: ETF didnt return the right value | " + err);
                    Log("Connection failed", "E");
                    return false;
                }
            }

            catch (SocketException te)
            {
                if (te.SocketErrorCode == SocketError.TimedOut)
                {
                    if (x < 3)
                    {
                        x++;
                        Console.WriteLine($"Socket_e: the connection timeouted... trying to reconect - attempts {x}/3");
                        Log($"Connection timedout, attempts {x}/3", "W");
                        return Connect(out err);
                    }
                    else
                    {
                        Console.WriteLine("con_conn: The number of tries is more than 2.\n" + te.Message);
                        Log("Number of attempts reached", "E");
                        err = "99:Connection failed";
                        return false;
                    }
                }

                else
                {
                    Log("Connection failed by timeout", "E");
                    err = "99:Connection failed by timeout";
                    return false;
                }
            }

            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                err = "99:Connection failed";
                return false;
            }
        }

        //---------------------------------- HandShake ----------------------------------

        /***************
         * @Documentation for HandShake
         * 
         * @HandShake function attempts to connect to the terminal and sends a Handshake request that verifies the succes of the connection
         * 
        ****************/

        /// <summary>
        /// Sends a Handshake request to the terminal to verify connection between you and terminal
        /// </summary>
        /// <param name="err"></param>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>

        public bool HandShake(out string response, out string err)
        {
            try
            {
                err = string.Empty;
                response = string.Empty;

                if (!Connect(out err)) return false;

                Log("Handshake", "M");
                NetworkStream networkStream = tcpClient.GetStream();
                string ProtocolVersion = "1";
                string data = $"{(int)Data_MSGtype.Request}{(string)DeviceID.SourceDev}{(string)DeviceID.DestinationDev}{ProtocolVersion}{(string)TransID.Handshake}01";
                byte[] request = Pack_Message(Create_Header((int)Header_MSGtype.Request), Encoding.UTF8.GetBytes(data));

                return WriteRead(networkStream, request, out response);
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                response = string.Empty;
                err = e.Message;
                throw new Exception(e.Message);
            }

        }

        //---------------------------------- Disconnect ----------------------------------

        /***************
         * @Documentation for Disconnect
         * 
         * @Disconnect function forces the program to disconnect from the terminal and flush any data left on networkStream
         * 
        ****************/

        /// <summary>
        /// Forces the program to disconnect from the terminal
        /// </summary>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>

        public bool Disconnect()
        {
            try
            {
                Console.WriteLine("Disconnecting...");
                Log("Disconnecting", "M");
                NetworkStream networkStream = tcpClient.GetStream();
                networkStream.Flush();
                networkStream.Close();
                Console.WriteLine("Succesful");
                return true;
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                throw new Exception(e.Message);
            }
        }

        //---------------------------------- Reconnect ----------------------------------

        /***************
         * @Documentation for Reconnect
         * 
         * @Reconnect function attempts to reconnect to the last known IP and PORT
         * 
        ****************/

        /// <summary>
        /// Attempts to reconnect to the last known IP and PORT
        /// </summary>
        /// <param name="err"></param>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>

        public bool Reconnect(out string err)
        {
            try
            {
                err = string.Empty;
                Log("Reconnecting", "M");
                Console.WriteLine("Reconnecting...");
                return Connect(out err);
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                throw new Exception(e.Message);
            }
        }

        //---------------------------------- Create_Header ----------------------------------

        /***************
         * @Documentation for Create_Header
         * 
         * @Create_Header is a functin to create a basic header for the message from the parameter of the message
         * 
        ****************/

        /// <summary>
        /// Creates a Header to be used in your message
        /// </summary>
        /// <param name="Type"></param>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>

        private byte[] Create_Header(int Type)
        {
            // <STX> NUM (MESSAGE HEADER) <FS> (NUM HEADER+PART OF MESSAGE) <FS> (REST OF MESSAGE) <ETX> (CRC1)(CRC2)
            // Message Header = MSG TYPE 2 | MSG FLAG 4 | MSG COUNTER 4

            try
            {
                MC = Convert.ToString(NUM);

                string s = $"0{Type}0000{new string('0', 4 - MC.Length)}{MC}";

                byte[] b = Encoding.UTF8.GetBytes(s);

                return b;
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                throw new Exception("Create_Header:" + e.Message);
            }
        }

        //---------------------------------- Create_Data ----------------------------------

        /***************
         * @Documentation for Data
         * 
         * @FS(byte) = 28
         * @System Number = Random generated 8-digit number from @GRN - it could overlap if two exactly the same numbers would be generated... but its highly unlikely
         * 
         * @GND function is GenerateRandomNumber, which returns randomly generated 8-digit number
         * @en function is just encoding for simplerer and neat err
         * @GetValueOrNull function finds the item in list that matches the given parameter and returns its value or if it doesnt exist it returns null
         * @ToSingleArr function converts List<byte[]> to a single array while ignoring any null items in it and keeping the order of the original list
         * 
        ****************/

        private int GRN()
        {
            int min = 10_000_000;
            int max = 100_000_000;
            Random r = new Random();

            return r.Next(min, max);
        }

        private byte[] en(string a)
        {
            if (a != null) return Encoding.UTF8.GetBytes(a);
            else return null;
        }

        private string GetValueOrNull(List<IFieldList> l, Type type)
        {
            var item = l.FirstOrDefault(x => x.GetType() == type);
            if (item != null)
            {
                return item.GetValue();
            }
            return null;
        }

        private byte[] ToSingleArr(List<byte[]> list)
        {
            return list.Where(x => x != null).SelectMany((x, i) => x.Select(b => new { Value = b, Index = i }))
                       .OrderBy(x => x.Index)
                       .Select(x => x.Value)
                       .ToArray();
        }

        /// <summary>
        /// Creates a list of data that is than packed into a byte array and returned
        /// </summary>
        /// <param name="l"></param>
        /// <param name="Rfn"></param>
        /// <returns>Data for the message to be send</returns>
        /// <exception cref="Exception"></exception>

        private byte[] Create_Data(List<IFieldList> l, string Rfn, bool same)
        {
            try
            {
                byte[] FS = new byte[] { (byte)ConChar.FS };

                // --- Data Header ---
                int MSGtype = (int)Data_MSGtype.Request;
                string desID = (string)DeviceID.DestinationDev;
                string souID = (string)DeviceID.SourceDev;
                string SystemNumber = "";
                if (!same) SystemNumber = Convert.ToString(GRN());
                else SystemNumber = SYSNUM;
                SYSNUM = SystemNumber;
                string ProtocolVersion = "1";
                string TrID = (string)TransID.Card_Service;
                string FlowFlag = (string)TP_FlowFlag.Print_receipt;      // td: PrintReciept

                // --- Data ---
                string Curr = GetValueOrNull(l, typeof(i_CurrencyCode));
                string Amount = GetValueOrNull(l, typeof(S_Amount));
                string Var_symbol = GetValueOrNull(l, typeof(s_VariableSymbol));
                string CardNum = GetValueOrNull(l, typeof(C_CardNum));
                string ExpDate = GetValueOrNull(l, typeof(e_ExpirationDate));
                string AuthCode = GetValueOrNull(l, typeof(a_AuthorizationCode));
                string LangCode = GetValueOrNull(l, typeof(l_LanguageCode));
                string SpecSymbol = GetValueOrNull(l, typeof(y_SpecificSymbol));
                string SeqNum = GetValueOrNull(l, typeof(q_SequenceNum));
                string AddAmm = GetValueOrNull(l, typeof(A_AddAmount));
                string RRN = GetValueOrNull(l, typeof(R_RRN));
                string Acquire = GetValueOrNull(l, typeof(r_Acquire));

                // --- Lightly packing data ---
                string s1 = $"{MSGtype}{souID}{desID}{ProtocolVersion}{TrID}{Rfn}";
                string s2 = $"{Curr}{Amount}";

                List<byte[]> by = new List<byte[]>();

                by.Add(en(s1));
                by.Add(en(CardNum));
                by.Add(FS);
                by.Add(en(ExpDate));
                by.Add(FS);
                by.Add(en(s2));
                by.Add(FS);
                by.Add(en(SystemNumber));
                by.Add(en(AuthCode));
                by.Add(FS);
                by.Add(en(FlowFlag));
                by.Add(FS);
                by.Add(en(LangCode));
                by.Add(FS);
                by.Add(en(Var_symbol));
                by.Add(FS);
                by.Add(en(SpecSymbol));
                by.Add(FS);
                by.Add(en(SeqNum));
                by.Add(FS);
                by.Add(en(AddAmm));
                by.Add(FS);
                by.Add(en(RRN));
                by.Add(FS);
                by.Add(en(Acquire));
                by.Add(FS);                         //add last few classes if needed
                by.Add(FS);
                by.Add(FS);
                by.Add(FS);

                byte[] b = ToSingleArr(by);

                return b;
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                throw new Exception("Create_Data:" + e.Message);
            }
        }

        //---------------------------------- Pack_Message ----------------------------------

        /***************
         * @Documentation for Pack_message
         * 
         * @Pack_message function creates a message by packing Header and Data with the rest of the required parameters as <STX> or CRC16
         * 
        ****************/

        /// <summary>
        /// Creates a message by packing Header and Data with the rest of the required parameters as STX or CRC16
        /// </summary>
        /// <param name="Header"></param>
        /// <param name="Data"></param>
        /// <returns>Returns a message to be send, created by packing the Header and Data of the message</returns>
        /// <exception cref="Exception"></exception>

        private byte[] Pack_Message(byte[] Header, byte[] Data)
        {
            try
            {
                byte STX = (byte)ConChar.STX;                        // 2
                byte ETX = (byte)ConChar.ETX;                        // 3
                NUM++;
                byte num = (byte)NUM;

                List<byte[]> bytes = new List<byte[]>();
                bytes.Add(new byte[] { STX });
                bytes.Add(new byte[] { num });
                bytes.Add(Header);
                bytes.Add(Data);
                bytes.Add(new byte[] { ETX });

                byte[] b = bytes.SelectMany(a => a).ToArray();

                Crc16 crc = new Crc16();
                byte[] CRC = crc.ComputeChecksumBytes(b.Skip(1).ToArray());

                byte[] request = b.Concat(CRC).ToArray();

                return request;
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                throw new Exception("Pack_Message:" + e.Message);
            }
        }

        //---------------------------------- Sale ----------------------------------

        /***************
         * @Documentation for Sale
         * 
         * @Sale function is used to send Sale request to the terminal, the out parameters returns either a terminal err or a error created by me or exception from VS
         * 
        ****************/

        /// <summary>
        /// Sends Sale request to the terminal of given ammount
        /// </summary>
        /// <param name="Amount">Max of 2 decimals</param>
        /// <param name="CurrencyCode">Can be the global curr code</param>
        /// <param name="VariableSymbol"></param>
        /// <param name="response">Self generated codes or terminal returned codes</param>
        /// <param name="err">Self generated exceptions or VS exception</param>
        /// <returns>Returns a bool value of which the Sale passed or not</returns>

        public bool Sale(string Amount, string CurrencyCode, string VariableSymbol, out string response, out string err)
        {
            try
            {
                Log("Sale", "M");
                string RefNum = ((char)Reference_number.E_REFNUM_P).ToString();

                /*Thread t = new Thread(() => {
                    string Tresponse;
                    string Terror;
                    int y = 0;
                    do
                    {
                        if (!tcpClient.Connected) tcpClient.Connect(IP, PORT);
                        Thread.Sleep(5000);
                        y++;
                        Console.WriteLine("Thread" + y);
                        SendRequest(Amount, CurrencyCode, VariableSymbol, RefNum, false, out Tresponse, out Terror);
                    } while (Tresponse.Contains("busy") || Tresponse.Contains("TERMI"));
                    
                });*/

                bool passed = SendRequest(Amount, CurrencyCode, VariableSymbol, RefNum, false, out response, out err);
                return passed;
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                err = e.Message;
                response = string.Empty;
                return false;
            }
        }

        //---------------------------------- Refund ----------------------------------

        /***************
         * @Documentation for Refund
         * 
         * @Refund is used to send refund request to the terminal by sending the ammount of which you want to refund, out parameters give either a self generated response code or err exception from VS
         * 
        ****************/

        /// <summary>
        /// Sends Refund request to the terminal of given ammount
        /// </summary>
        /// <param name="Amount">The ammount you want to refund</param>
        /// <param name="CurrencyCode"></param>
        /// <param name="VariableSymbol"></param>
        /// <param name="response">Self generated codes or terminal returned codes</param>
        /// <param name="err">Self generated exceptions or VS exception</param>
        /// <returns>Returns a bool value of which the Refund passed or not</returns>

        public bool Refund(string Amount, string CurrencyCode, string VariableSymbol, out string response, out string err)
        {
            try
            {
                Log("Refund", "M");
                string RefNum = ((char)Reference_number.E_REFNUM_R).ToString();
                return SendRequest(Amount, CurrencyCode, VariableSymbol, RefNum, false, out response, out err);
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                err = e.Message;
                response = string.Empty;
                return false;
            }
        }

        //---------------------------------- Reversal ----------------------------------

        /***************
         * @Documentation for Reversal
         * 
         * @Reversal not used
         * 
        ****************/

        /// <summary>
        /// Not Used
        /// </summary>
        /// <param name="Amount">The ammount you want to refund</param>
        /// <param name="CurrencyCode"></param>
        /// <param name="VariableSymbol"></param>
        /// <param name="response">Self generated codes or terminal returned codes</param>
        /// <param name="err">Self generated exceptions or VS exception</param>
        /// <returns>Returns a bool value of which the Refund passed or not</returns>

        public bool Reversal(string Amount, string CurrencyCode, string VariableSymbol, out string response, out string err)
        {
            try
            {
                Log("Reversal", "M");
                string RefNum = ((char)Reference_number.E_REFNUM_X).ToString();
                return SendRequest(Amount, CurrencyCode, VariableSymbol, RefNum, true, out response, out err);
            }
            catch (Exception e)
            {
                Log($"{e.Message}", "E");
                err = e.Message;
                response = string.Empty;
                return false;
            }
        }

        //---------------------------------- ReprintReciept ----------------------------------

        /***************
         * @Documentation for ReprintReciept
         * 
         * @ReprintRecipt Reprints the Reciept from the last transaction
         * 
        ****************/

        /// <summary>
        /// Reprints the Reciept from the last transaction
        /// </summary>
        /// <param name="response"></param>
        /// <param name="err"></param>
        /// <returns></returns>

        public bool ReprintReciept(out string response, out string err)
        {
            try
            {
                Log("Reprint Reciept", "M");
                response = string.Empty;
                err = string.Empty;
                bool passed;

                if (!Connect(out response))
                {
                    return false;
                }

                int MSGtype = (int)Data_MSGtype.Request;
                string desID = (string)DeviceID.DestinationDev;
                string souID = (string)DeviceID.SourceDev;
                string SystemNumber = SYSNUM;                               
                string ProtocolVersion = "1";
                string TrID = (string)TransID.Reprint_Reciept;
                string FlowFlag = (string)TP_FlowFlag.Print_receipt;

                NetworkStream stream = tcpClient.GetStream();

                string s1 = $"{MSGtype}{souID}{desID}{ProtocolVersion}{TrID}{SystemNumber}{FlowFlag}";

                byte[] header = Create_Header((int)Header_MSGtype.Request);
                byte[] data = en(s1);

                byte[] request = Pack_Message(header, data);

                passed = WriteRead(stream, request, out response);

                return passed;
            }
            catch (Exception e)
            {
                err = e.Message;
                response = string.Empty;
                return false;
            }
        }


        //---------------------------------- SendRequest ----------------------------------

        /***************
         * @Documentation for Send_request
         * 
         * @SendRequest this finction sends a message given as a request to the terminal with the given ReferenceNumber
         * 
        ****************/

        /// <summary>
        /// Sends a request to the terminal with given ReferenceNumber
        /// </summary>
        /// <param name="Amount"></param>
        /// <param name="CurrencyCode"></param>
        /// <param name="VariableSymbol"></param>
        /// <param name="RefNum"></param>
        /// <param name="response"></param>
        /// <param name="err"></param>
        /// <returns></returns>

        private bool SendRequest(string Amount, string CurrencyCode, string VariableSymbol, string RefNum, bool same, out string response, out string err)
        {

            try
            {
                response = string.Empty;
                err = string.Empty;
                bool passed;

                if (!Connect(out response))
                {
                    return false;
                }

                NetworkStream stream = tcpClient.GetStream();

                List<IFieldList> parameters = new List<IFieldList>();

                parameters.Add(new S_Amount(Amount));
                parameters.Add(new i_CurrencyCode(CurrencyCode));
                parameters.Add(new s_VariableSymbol(VariableSymbol));

                string Rfn = RefNum;

                var header = Create_Header((int)Header_MSGtype.Request);
                var data = Create_Data(parameters, Rfn, same);

                byte[] request = Pack_Message(header, data);

                passed = WriteRead(stream, request, out response);

                if (response == "") response = "02:Device is busy";

                //Disconnect();

                return passed;
            }
            catch (Exception e)
            {
                err = e.Message;
                response = string.Empty;
                return false;
            }

        }

        //===============================================================================================

        //------------------------------------ ToStringConvertors ---------------------------------------

        /// <summary>
        /// Converts bytes to string using UTF8 encoding and converting the special characters to their string representation as well - 28 = FS 
        /// </summary>
        /// <param name="bytes">The byte array data you want to convert to message</param>
        /// <returns></returns>

        private List<string> ToMSG(byte[] bytes)
        {
            List<string> l = new List<string>();

            foreach(byte b in bytes)
            {
                if (b == 2) l.Add("<STX>");
                else if (b == 28) l.Add("<FS>");
                else if (b == 3) l.Add("<ETX>");
                else if (b == 6) l.Add("<ACK>");
                else if (b == 21) l.Add("<NAK>");
                else if (b == 5) l.Add("<ENQ>");
                else if (b == 4) l.Add("<EOT>");
                else if (b == 0) continue;
                else
                {
                    l.Add(Encoding.UTF8.GetString(new[] { b }));
                }

            }

            return l;
        }

        /// <summary>
        /// Converts the data from string to a hex message representation which is used in most documentation or logs
        /// </summary>
        /// <param name="s"></param>
        /// <returns></returns>

        private List<string> ToHex(List<string> s)
        {
            List<string> l = new List<string>();

            foreach(string b in s)
            {
                if (b == "<STX>") l.Add("02");
                else if (b == "<FS>") l.Add("1c");
                else if (b == "<ETX>") l.Add("03");
                else if (b == "<ACK>") l.Add("06");
                else if (b == "<NAK>") l.Add("21");
                else if (b == "<ENQ>") l.Add("05");
                else if (b == "<EOT>") l.Add("04");
                else if (b == "<DLE>") l.Add("10");
                else if (b == "<WACK>") l.Add("13");
                else if (b == "<EOT>") l.Add("1D");
                else
                {
                    byte[] ba = Encoding.UTF8.GetBytes(b);
                    var hexString = BitConverter.ToString(ba);
                    hexString = hexString.Replace("-", "");
                    l.Add(hexString);
                }
            }

            return l;
        }

        //------------------------------------ FromStringConvertors ---------------------------------------

        /// <summary>
        /// Converts the data from hex representation to bytes which you can than send to the terminal
        /// </summary>
        /// <param name="s"></param>
        /// <returns></returns>

        private byte[] FromHex(List<string> s)
        {
            List<byte> l = new List<byte>();

            foreach(string b in s)
            {
                l.Add(Convert.ToByte(b, 16));
            }

            return l.ToArray();
        }

        //-------------------------------- CRC16 calculations -------------------------------------------

        /// <summary>
        /// Class used to get CRC1 and CRC2 which is used to control the correction of sent or recived message
        /// </summary>

        public class Crc16
        {
            const ushort polynomial = 0xA001;
            ushort[] table = new ushort[2048];

            /// <summary>
            /// Calculates the CRC16 sum of the bytes given
            /// </summary>
            /// <param name="bytes"></param>
            /// <returns>ushort sum of given data</returns>
            protected ushort ComputeChecksum(byte[] bytes)
            {
                ushort crc = 0;
                for (int i = 0; i < bytes.Length; ++i)
                {
                    byte index = (byte)(crc ^ bytes[i]);
                    crc = (ushort)((crc >> 8) ^ table[index]);
                }
                return crc;
            }

            /// <summary>
            /// Convers the ushort sum of CRC16 to byte[]
            /// </summary>
            /// <param name="bytes"></param>
            /// <returns>byte[2] of given data</returns>
            public byte[] ComputeChecksumBytes(byte[] bytes)
            {
                ushort crc = ComputeChecksum(bytes);
                return BitConverter.GetBytes(crc);
            }

            public Crc16()
            {
                ushort value;
                ushort temp;
                for (ushort i = 0; i < table.Length; ++i)
                {
                    value = 0;
                    temp = i;
                    for (byte j = 0; j < 8; ++j)
                    {
                        if (((value ^ temp) & 0x0001) != 0)
                        {
                            value = (ushort)((value >> 1) ^ polynomial);
                        }
                        else
                        {
                            value >>= 1;
                        }
                        temp >>= 1;
                    }
                    table[i] = value;
                }
            }
        }

        //=========================================================== LOG ============================================================

        /*****************
         * @Documentation for LOG
         * 
         * @Log is a function that logs the process of the program to the locat Documents file LOG.txt with [Parameter][Date]
         * 
         * [M] - Basic info message
         * [S] - Message sent to terminal
         * [R] - Message recived from terminal
         * [W] - Warning from program
         * [E] - Error from program
         * [T] - Error from terminal
         * 
        ******************/

        /// <summary>
        /// Logs the program process to a local Documents file LOG.txt
        /// </summary>
        /// <param name="msg"></param>
        /// <param name="parameter"></param>
        private void Log(string msg, string parameter)
        {
            string date = DateTime.Now.ToString("dd.MM.yyyy-HH:mm:ss");
            if (!File.Exists(file)) File.AppendAllText(file, "[M] - Basic info message\n[S] - Message sent to terminal\n[R] - Message recived from terminal\n[W] - Warning from program\n[E] - Error from program\n[T] - Error from terminal");
            File.AppendAllText(file, $"[{parameter}][{date}]=> " + msg + "\n", Encoding.UTF8);
        }
    }
}
