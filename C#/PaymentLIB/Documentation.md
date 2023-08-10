# My payment LIB - DLL

## Objective

The aim of my thesis is to create a functional DLL library in C# for communicating with a payment terminal for credit card payments. This project was assigned to me at the company, and I am very satisfied with it. I have always been curious about how such a DLL library is written and what challenges I might face in the process. I plan to further enhance this library with functions that were not initially implemented. The library is designed for ease of use and can also be used in other programming languages, as I've enabled COM. The library will use bytes to transmit data between the user and the terminal, which is interesting as I've never done anything similar before. I have received documentation that I will follow. It contains information on how the terminal processes data, both directly and in what format it should be sent.

My library will be a C# .dll for communication with the payment terminal, serving as an intermediary between the user and the terminal. I've implemented only the functions requested by the client. The library provides 5 functions: Sale, Refund, HandShake, ReceiptReprint, and SetIPnPORT. The first function to be used must always be SetIPnPORT, so the library knows where to connect and communicate.

I intend to achieve this goal primarily by utilizing my existing skills, which I believe will be sufficient for most of the work. However, I also plan to use the internet for documentation on TcpClient, which I intend to use for communication.

## Object Design

### Terminal

The Terminal is the main non-static class in my library, where all the functions are implemented. These functions are further mapped to the IPayment interface, making them callable. All parameters sent to the terminal are handled through classes in an abstract class, allowing for pre-use validation.

## Methods

- `private bool msg_write(NetworkStream networkStream, byte[] Msg)` – attempts to send a message to the terminal.

- `private bool WriteRead(NetworkStream networkStream, byte[] Message, out string code)` – attempts to send a message to the terminal, then reads the response, with 3 attempts spaced 500ms apart.

- `private byte[] msg_read(NetworkStream networkStream)` – attempts to read a message from the terminal.

- `private bool send_ACK(NetworkStream networkStream)` – sends an ACK byte to confirm with the terminal.

- `private bool send_NAK(NetworkStream networkStream)` – sends a NAK byte to the terminal for rejection.
- `public bool SetIPnPORT(string ip, int port)` – sets the IP and PORT for the connection.
- `private bool Connect(out string err)` – attempts to connect to the terminal using the set IP and PORT, with 3 attempts spaced 1.5 seconds apart.
- `public bool HandShake(out string response, out string err)` – checks the connection between the terminal and the client.
- `public bool Disconnect()` – disconnects from the terminal.
- `public bool Reconnect(out string err)` – reconnects to the last used IP and PORT.
- `private byte[] Create_Header(int Type)` – creates a message header.
- `private int GRN()` – generates a random number for the system number sent in data.
- `private byte[] en(string a)` – encodes a message into UTF8 bytes.
- `private string GetValueOrNull(List<IFieldList> l, Type type)` – returns a value of a given type from a list or null.
- `private byte[] ToSingleArr(List<byte[]> list)` – transforms a list of byte arrays into a single array while preserving their order.
- `private byte[] Create_Data(List<IFieldList> l, string Rfn, bool same)` – creates data from a list for the message.
- `private byte[] Pack_Message(byte[] Header, byte[] Data)` – combines data and header into a single message for the terminal.
- `public bool Sale(string Amount, string CurrencyCode, string VariableSymbol, out string response, out string err)` – sends a payment request to the terminal.
- `public bool Refund(string Amount, string CurrencyCode, string VariableSymbol, out string response, out string err)` – sends a refund request to the terminal.
- `public bool Reversal(string Amount, string CurrencyCode, string VariableSymbol, out string response, out string err)` – cancels the last payment.
- `public bool ReprintReceipt(out string response, out string err)` – reprints the last receipt.
- `private bool SendRequest(string Amount, string CurrencyCode, string VariableSymbol, string RefNum, bool same, out string response, out string err)` – sends a request for a value and receives it.
- `private List<string> ToMSG(byte[] bytes)` – converts a byte array to a string list.
- `private List<string> ToHex(List<string> s)` – converts normal text to hexadecimal.
- `private byte[] FromHex(List<string> s)` – converts hexadecimal to byte array.

### Crc16 Class

A class utilized for generating CRC (Cyclic Redundancy Check), used at the end of the message for transmission control.

## Parameter Variables

Variables used for parameter validation before being stored in a specific type. Validation options are:

- A (Alphabetic characters)
- N (Numeric characters)
- S (Special characters)

Validator function in FieldListBase iterates through the parameters to check if the characters match the allowed ones.

- `A_AddAmount – N, 1–10`
- `a_AuthorizationCode – AN, 1–8`
- `B_CardBrand – AN, 1–15`
- `C_CardNum – NS, 3–19`
- `c_TransAmount – N, 1–12`
- `D_TermID – AN, 8–18`
- `d_TransCountcs – N, 1–9`
- `e_ExpirationDate – N, 4`
- `H_CardHash – AN, 40`
- `i_CurrencyCode – N, 2–3`
- `I_TranslD – N, 1–9`
- `I_LanguageCode – N, 2`
- `q_SequenceNum – N, 1–10`
- `r_Acquire – N, 2`
- `R_RRN – AN, 1–12`
- `S_Amount – N, 1–10`
- `s_VariableSymbol – N, 1–10`
- `y_SpecificSymbol – N, 1–10`

## Communication with the Terminal

Communication with the terminal was initially challenging as I had no understanding of bytes, which are used for terminal communication. I received documentation that defined the purpose of various bytes and their quantities for different scenarios. The terminal itself offers numerous options for different messages, ranging from basic card payments, refunds, and payment cancellations to handshakes and pre-authorized payments. Each of these scenarios has distinct parameters and terminal responses.

### Example SALE – Basic Payment

#### Header

The message header must include the message type, message flag, and message counter. In this case, the message type is a request (byte 01), the flag is reserved for future messages (0000), and the counter indicates the message number (0000).

#### Data

The next step is to create the actual message data. Data also has its header, with default values often specified in the documentation. One of the most important parameters in the data is the transaction ID, which determines the type of service. In this case, it's Card_Service (76). Following that is a value indicating the type of message, where SALE is represented by the letter P. The next parameter is the currency code, which needs conversion from global codes to terminal-specific codes because the terminal uses its own codes. We then include the payment amount, which requires careful handling. If the amount is a whole number, two zeros are added at the end. If the amount includes decimals, a comma is used to separate the decimal part. There are many optional parameters and additional aspects to consider, but these are the fundamental basics.

#### Sending

Once the message is constructed, it needs to be sent to the terminal. This involves converting the message into bytes and sending it to the terminal using the TCP protocol. We then wait for a response from the terminal to determine the outcome of the payment, allowing us to return a specific code and message.

## RESUMÉ

The goal of my work was to create a functional DLL Library in C# to communicate with a payment terminal for credit card payments. This project was assigned to me in the company, and I am very satisfied with it. I have always wondered how such a DLL library is written and what challenges it presents throughout the process.

My intention is to further expand this library to include functions that were not initially part of the scope. The library itself is designed to be user-friendly and versatile, making it suitable for integration into various programming languages with the inclusion of COM. The library facilitates data transmission between users and the terminal, which was a fascinating aspect since I had never worked on something similar before.

Each stage of this project has contributed significantly to my wealth of experience and skills, empowering me for future library and program development to meet client needs. It has also deepened my understanding of C# programming and communication at the byte level. In the future, I aspire to complete this project or embark on other projects focusing on byte-level communication between clients and servers.

If I were to continue this work, I would encompass the incorporation of various payment methods and additional message types. I would develop a custom graphical user interface (GUI) for the library and optimize it by implementing asynchronous functions while ensuring a user-friendly interface to access classes and functions.
