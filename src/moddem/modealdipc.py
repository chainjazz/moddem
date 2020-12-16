'''
Created on 21 Apr 2020

@author: dkr85djo
'''
import sys
import selectors
import socket
import ssl
import os
import xml.etree.ElementTree as ET

from moddem.modealhttp import MDHttp
import struct

class MDGameIPC:
    def __init__(self, gamestate, hname='ionian', hport=24571, baseuri=''):
        self.sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.sslcontext.load_cert_chain(
            certfile="../../productionchain.pem", 
            keyfile="../../sub-ca_server.key")        
        self.sslcontext.verify_mode = ssl.CERT_NONE
        
        self.sslcontext.options |= ssl.OP_NO_TLSv1
        self.sslcontext.options |= ssl.OP_NO_TLSv1_1        
        self.sslcontext.options |= ssl.OP_NO_TLSv1_3
        self.sslcontext.set_ciphers('ECDHE-RSA-AES128-GCM-SHA256')
        self.sslcontext.set_alpn_protocols(['spdy/2', 'h2'])
        
        self.rhosts = 0
        self.gamestate = gamestate        
        self.hname = hname
        self.hport = hport        
        self.hselector = selectors.DefaultSelector()
        self.sock = None # main server socket
        self.conns = [] # client sockets (physical, used for debugging TCP/HTTP)
        self.http = MDHttp( 
            # CORS whitelist (incoming)
            [
                hname.encode(),
                b'192.168.0.35', 
                b'batenga.ddns.net',
                b'hypolydian'
             ],
            staticbaseuri=baseuri
            )
         
        
    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        rport = conn.getpeername()[1]                
        conn.do_handshake()
        print("Cipher: " + str(conn.cipher())) 
        conn.setblocking(False)       
        self.hselector.register(conn, selectors.EVENT_READ, self.read)
        
        if rport not in self.conns:
            self.conns.append(rport)
            print ("+[" + str(rport) + "]")
        else:
            print ("=[" + str(rport) + "]")
        
    
    def read(self, conn, mask):
        if self.http.h2 == True: # h2         
            data = conn.recv(struct.calcsize(">LBL"))
            
            if len(data) > 0:
                data = conn.recv(self.http.h2_frame_unwrap(data))
            (udata,) = struct.unpack(">" + str(len(data)) + "s", data)
            print(udata) #
            self.http.parse_request(udata)
            
        elif self.http.h2 == False:
            data = conn.recv(24)  # preface h2
            
            if data == self.http.H2_PREFACE: # h2 or http11
                data = conn.recv(struct.calcsize(">LBL")) # frame header
                data = conn.recv(self.http.h2_frame_unwrap(data)) # frame payload
            
                self.http.response = self.http.h2_frame_wrapper(
                    b'', self.http.frame_types['SETTINGS'], self.http.frame_flags['ACK'], 0x0) + b''
            
                conn.send(self.http.response)
                self.http.h2 = True
            
        elif (self.http.request) and self.gamestate.gameon == False:            
            # TODO: FIXME: DANGEROUS TESTING; USE EXPLICIT REGEXP!!!
            if (b'join_game' in self.http.request):
                pcookie = self.http.getcookie(b'modealc_pname')
                phandle = self.http.getparam(b'reqid')
                pname = self.http.getparam(b'pname')
                
                if (pcookie == None):
                    self.http.setcookie('modealc_pname', phandle.decode(), '86400')
                else:
                    print(pcookie)
                    phandle = pcookie # set is textmode, get is binary
                    
                self.gamestate.induct_player(phandle, pname, conn)
                self.http.response_payload = self.gamestate.tostring()              
            elif b'get_state' in self.http.request:            
                pcookie = self.http.getcookie(b'modealc_pname')
                self.http.response_payload = self.gamestate.tostring(tailoredfor=pcookie)       
            elif (b'start_game' in self.http.request) and (len(self.gamestate.players) > 1):
                # interrupt Assembly loop in MDGameState
                self.gamestate.startRequest = True
            else:
                self.http.retreive_static() 
            
            self.http.setresponse()
            conn.send(self.http.response)
            
        elif (self.http.request) and self.gamestate.gameon == True:            
            if      (b'halt_game' in self.http.request):
                self.gamestate.set_game_state(False)               
            elif    (b'get_state' in self.http.request):
                pcookie = self.http.getcookie(b'modealc_pname')
                
                if pcookie == b'':
                    pcookie = None
                #self.gamestate.reload_player(pcookie, conn)
                              
                self.gamestate.update_game_state()
                
                for p in self.gamestate.players:
                    if p.handle == pcookie:
                        p.dirty = False
                            
                self.http.response_payload = self.gamestate.tostring(tailoredfor=pcookie)           
            
            self.http.setresponse()
            conn.send(self.http.response)
            
        else:
            self.daemon_closeconn(conn)            
        
    def daemon_openconn(self):
        events = self.hselector.select() # non blocking server boilerplate
        
        try:
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
        except KeyError:
            raise
        except OSError:
            raise               
                
    def daemon_closeconn(self, conn):
        # note: if using conn in debug output,
        # it needs to be inside try clause        
        try:            
            self.hselector.unregister(conn)
            conn.close()            
        except KeyError:
            print ("Verify disconnect OK.")
        except OSError:
            print("Bad socket descriptor.")
    
    def daemon_reset(self):
        self.gamestate.reset_game_state()
        # careful here, circular function call
        self.gamestate.game_loop(self)
               
    def daemon_shutdown(self):
        #for c in self.conns:            
            # self.daemon_closeconn(c)
        
        self.daemon_reset()           
    
    def daemon_kill(self):  
        print("Server shutdown\n", self.sock.getsockname())        
        self.daemon_closeconn(self.sock)  
        
    def daemon_deploy(self):
        # _boilerplate_
        
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        
        sock.bind((self.hname, self.hport))      
        self.sock = self.sslcontext.wrap_socket(sock, server_side=True, do_handshake_on_connect=False)
         
        self.sock.listen(100)
        self.sock.setblocking(False) 
        self.hselector.register(self.sock, selectors.EVENT_READ, self.accept)       
                              
        self.gamestate.game_loop(self) 
        # TODO: reset gamestate and return daemon to assembling players
                
        