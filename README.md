# Text service
 
A command line application that offers 2 services: Vernam encryption and swapping words. Communication between client and server is made over TCP channel. 

![Screenshot of running test.py](https://github.com/vuusale/text_service/blob/master/screenshot.png)

## Prerequisites
It is required to have Python3 installed in order to run the application. Just go to the [official Python website](https://python.org/) and download the release suitable to your machine. For example, if you have 64-bit Windows operating system, download *Windows x86-64 executable installer*. 

After ensuring that Python3 is set up, follow the below steps:

- Clone the repository into a desired location:
  
      $ git clone https://github.com/vuusale/text_service.git
      
- Install the requirements:
  
      $ pip install -r requirements.txt
  
Now you are ready to run the program. 

## Usage
Open 2 terminals: one for server and one for client. Then, run the following command in the first tab for server setup:
  
    $ python3 server.py
  
To use one of the services as client, run below command in the second terminal:
    
    $ python3 client.py -m MODE -t TEXT_FILE -k KEY_OR_JSON_FILE
   
#### Options:
<ul>
  <li>-m, --mode: Specify the service type. For Vernam encryption, choose "encode_decode". For swapping words based on a JSON file, choose "change_text"</li>
  <li>-t, --text_file: Specify the path to the text file</li>
  <li>-k, --jk_file: Specify the path to the JSON or key file</li>
</ul>

## Services

#### Change_text
In this mode, words in the text file are swapped according to the JSON file. Structure of the JSON file is as following:

      {
          "word_to_change": "new_word",
          ...
      }

#### Encode_decode
In this mode, bitwise XOR operation is performed on the text and key file contents. This encryption is known as **Vernam cipher**.

##### Vernam cipher
Vernam cipher is based on the principle that each plaintext character from a message is mixed with the corresponding character from a key stream. For this cipher, both the plaintext and the key must have the same length. 

If a truly random key stream is used, the result will be a truly 'random' ciphertext which bears no relation to the original plaintext. In order to achieve utmost security, the encryption keys should be used only once, that's why it is called **One-Time Pad (OTP)**. 

In this application, The OTP can be generated using *gen_otp.py* file. It checks the length of the file that OTP is created for, and a random string of ASCII characters with the same length, including numbers, lowercase/uppercase letters and punctuation marks, is generated and saved to the output file. Its usage is basic: `python3 gen_otp.py -f FILE -o OUTPUT`.

The server first encrypts the plaintext using Vernam cipher, and sends it to the client. Afterwards, it applies the same cipher on the result and sends it to the client for verification (this is done just for the sake of the task). The key concept here is that XOR can be reverted according to the following rule:

     plaintext + key = ciphertext ⇒ ciphertext + key = plaintext 

###### XOR truth table
![XOR truth table](https://www.electrical4u.com/images/january16/1454933398.GIF)

In mathematics, the XOR operation is known as modulo-2 addition. In our case, the individual bits of the plaintext are XOR-ed with the individual bits of the key. The resulting bit will be '1' if the two input bits are different. If they are equal (both 1 or both 0), the result will be '0'. In fact, each bit from the key tells us whether or not the corresponding bit from the plaintext should be inverted. By inverting these key-bits again, the original character is revealed.
