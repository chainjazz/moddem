'''
Created on 28 Apr 2020

@author: dkr85djo
'''
from datetime import datetime as DT
from datetime import timezone as TZ
from _collections_abc import list_iterator
import struct

class MDHttp:
    def __init__(self, proxylist, staticbaseuri='../../../public_html'):
        self.request = b''
        self.request_method = b'' # for extending http with new methods/actions
        self.request_resource = b''
        self.request_protocol = b''
        self.request_headers = b''
        self.request_payload = b''
        self.response = b''
        self.response_contenttype = b''
        self.response_headers = b''
        self.response_cookies = []
        self.response_payload = b''
        self.proxy_list = proxylist
        self.allow_origin = False
        self.static_base_uri = staticbaseuri
        self.mime_types = {
            b'xml' : b'application/xml',
            b'html' : b'text/html',
            b'js'    : b'text/javascript',
            b'png'   : b'image/png',
            b'svg'   : b'image/svg+xml',
            b'css'  : b'text/css',
            b'xsl'  : b'text/xsl'            
            }
        self.aliases = {
            'lib'   : '../../../lib',
            'xmldb' : '../../../xmldb',
            'res'   : '../../../res'
            }
        self.frame_types = {
            'DATA'      : 0x0,
            'HEADERS'   : 0x1,
            'PRIORITY'  : 0x2,
            'RST_STREAM': 0x3,
            'SETTINGS'  : 0x4,
            'PUSH_PROMISE' : 0x5,
            'PING'      : 0x6,
            'GOAWAY'    : 0x7,
            'WINDOW_UPDATE' : 0x8,
            'CONTINUATION' : 0x9            
            }
        self.frame_flags = {
            'END_STREAM'    : 0x1,
            'END_HEADERS'   : 0x4,
            'ACK'           : 0x1
            }
        self.H2_PREFACE = b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n'  
        self.h2 = False 
    
    def checkorigin(self, hname, hport):
        forwarded_by = self.getheader(b'X-Forwarded-Server')
        whoami = self.getheader(b'Host')
        whoareyou = self.getheader(b'Origin')
        whoshouldibe = hname.encode() + b':' + str(hport).encode() # TODO: self?
                
        if forwarded_by in self.proxy_list:        
            self.allow_origin = whoareyou
        elif whoami == whoshouldibe:
            self.allow_origin = whoareyou
        elif whoareyou:
            print("Request origin denied from ", whoareyou)
        else:            
            self.allow_origin = False
            
    
    def parse_request(self, req):        
        self.request_headers = req.split(b'\n')
        
        #print("Request Headers:\n" + str(self.request_headers))
        
        self.request_method = self.getheader(b':method')
        self.request_resource = self.getheader(b':path')
        self.request_protocol = self.getheader(b':scheme') 
       
        # TODO: if method POST, retrieve payload
        
    def retreive_static(self):
        rcontenttype = None
        rcontentpath = None 
        rbaseuri = self.static_base_uri
        bdata = None
        
        if self.request_resource:
            self.request_resource.split(b'.')[1]
        else:
            return
        
        if (rcontenttype in self.mime_types):
            self.response_contenttype = self.mime_types[rcontenttype]
        
        try:
            bdata = open(rbaseuri + self.request_resource.decode(), mode='rb')
        except FileNotFoundError:
            rcontentpath = self.request_resource.split(b'/', maxsplit=2)
            
            if (rcontentpath[1].decode() in self.aliases):
                rbaseuri = self.aliases[rcontentpath[1].decode()]
                bdata = open(rbaseuri + "/" + rcontentpath[2].decode(), mode='rb')
                
        if (bdata):
            self.response_payload = bdata.read()
            bdata.close()
    
    
    def h2_frame_wrapper(self, in_fpayload, ftype=0x00, fflags=0x00, streamid=0x00000000):        
        nineoctets = struct.pack('>LBL', len(in_fpayload) * 0xff + ftype, fflags, streamid)
        return nineoctets + in_fpayload
    
    def h2_frame_unwrap(self, f):
        (flenandtype, fflags, fstreamid) = struct.unpack(">LBL", f)
        plen = round(flenandtype >> 8)
        ftype = flenandtype & 0x0ff
        streamid = fstreamid & 0xefffffff       
        
        for (k, v) in iter(self.frame_types.items()):
            if ftype == v:               
                print("R" + str(streamid) + ": [" + k + "]\t\t[ " + str(plen) + "b ]")
                return plen
        
        return 0
            
    def getheader(self, header_name):
        multiheader = [] # headers that appear several times, like Cookie
        
        for h in self.request_headers: # NOTFUNNY: as long as it's iterable
            if header_name in h.split(b': ', maxsplit=1)[0]:
                multiheader.append(h.split(b': ', maxsplit=1)[1])
        
        if len(multiheader) == 1:
            return multiheader[0]
        elif len(multiheader) > 1:
            return multiheader # NOTFUNNY: returning array
        else:
            return None
        
    def getparam(self, paramname):
        (req,sep,spec) = self.request_resource.partition(b'?')
        params = spec.split(sep=b'&') #TODO: or null if only one param
        
        for p in params:
            if paramname in p:
                return p.split(b'=', maxsplit=1)[1].split()[0]
            
        return None
            
    def getcookie(self, name):
        cookies = []
        headers = self.getheader(b'cookie')                
        
        # TODO: FIXME (wasteful typechecking)
        #    self.getheader always returns either a list or string (list)        
        if headers == [] or headers == None:
            return None # some heavy duty type checking
        elif headers is list:
            cookies.extend(headers)            
        else:
            cookies.append(headers)
        
        for c in cookies:
            if name in c.split(b'=', maxsplit=1)[0]:
                return c.split(b'=', maxsplit=1)[1]
            
        return None
                                        
    
    def setcookie(self, name, value, expires_in_sec, cookie_prefix=b'__Host-'):
        la_patisserie = (cookie_prefix +
            name.encode() + b'=' + value.encode() + b';' +
            b'Max-Age=' + expires_in_sec.encode() + b';' +
            b'Path=/;' +
            b'SameSite=Lax;' +
            b'HttpOnly' +   
            b'Secure'
            )
        self.response_cookies.append(la_patisserie)
        
    def setheader(self, name, value):
        self.response_headers += (
            name.encode() + b' = ' + value.encode() + b'\n'
            )
        
    def setresponse(self, status='200', close=''):
        # note we clear headers here
        self.response_headers = b''
        self.setheader(":status", status)
        
        if (self.allow_origin):
            self.setheader("access-control-allow-origin", 
                                self.allow_origin.decode())
        self.setheader('accept-ranges', 'bytes')    
        self.setheader('access-control-allow-credentials', 'true')
        self.setheader("date", DT.now(TZ.utc).
                            strftime('%a, %d %b %Y %H:%M:%S GMT'))        
        self.setheader("content-type", self.response_contenttype.decode())
        self.setheader("content-length",
                            str(len(self.response_payload)))       
        #self.setheader("cache-control", "no-cache")
        #self.setheader("strict-transport-security", "max-age=2592000")
        #self.setheader("location", "https://ionian:24571/")
        #self.setheader("vary", "Upgrade-Insecure-Requests")
        self.setheader("server", "Monopoly Deal Server 0.9")
        
        for pain in self.response_cookies:
            self.setheader('cookie', pain.decode())
                
        # self.response_headers += b'\r\n'        
        self.response = self.h2_frame_wrapper(
            self.response_headers, 
            self.frame_types['HEADERS'], 
            self.frame_flags['END_HEADERS'], 3) + self.h2_frame_wrapper(
                self.response_payload, 
                self.frame_types['DATA'], 
                self.frame_flags['END_STREAM'], 3)
        
        # clear cookies after compiling response
        # (for each request/response cycle)
        self.response_cookies = []
        self.response_payload = b''       