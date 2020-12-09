'''
Created on 25 Aug 2020

@author: dkr85djo
'''
import struct

field_static = [ 
            [b'1based',     b''],
            [b':authority', b''],
            [b':method',                        b'GET'],
            [b':method',                        b'POST'],
            [b':path',                          b'/'],
            [b':path',                          b'/index.html'],
            [b'scheme',                         b'http'],
            [b'scheme',                         b'https'],
            [b'status',                         b'200'],
            [b'status',                         b'204'],
            [b'status',                         b'206'],
            [b'status',                         b'304'],
            [b'status',                         b'400'],
            [b'status',                         b'404'],
            [b'status',                         b'500'],
            [b'accept-charset',                 b''],
            [b'accept-encoding',                b'gzip,deflate'],
            [b'accept-language',                b''],
            [b'accept-ranges',                  b''],
            [b'accept',                         b''],
            [b'access-control-allow-origin',    b''],
            [b'age',                            b''],
            [b'allow',                          b''],
            [b'authorization',                  b''],
            [b'cache-control',                  b''],
            [b'content-disposition',            b''],
            [b'content-encoding',               b''],
            [b'content-langauge',               b''],
            [b'content-length',                 b''],
            [b'content-location',               b''],
            [b'content-range',                  b''],
            [b'content-type',                   b''],
            [b'cookie',                         b''],
            [b'date',         b''],
            [b'etag',         b''],
            [b'expect',         b''],
            [b'expires',         b''],
            [b'from',         b''],
            [b'host',         b''],
            [b'if-match',         b''],
            [b'if-modified-since',         b''],
            [b'if-none-match',         b''],
            [b'if-range',         b''],
            [b'if-unmodified-since',         b''],
            [b'last-modified',         b''],
            [b'link',         b''],
            [b'location',         b''],
            [b'max-forwards',         b''],
            [b'proxy-authenticate',         b''],
            [b'proxy-authorization',         b''],
            [b'range', b''],
            [b'referer', b''],
            [b'refresh',  b''],
            [b'retry-after', b''],
            [b'server', b''],
            [b'set-cookie', b''],
            [b'strict-transport-security', b''],
            [b'transfer-encoding', b''],
            [b'user-agent', b''],
            [b'vary', b''],
            [b'via', b''],
            [b'www-authenticate', b'']           
        ]

class h2int:
    # basically, implements BIGINT
    def __init__(self, initv=0, octet_offset=0):
        self.v = initv
        self.N = 8 - octet_offset
        
    def encode(self):
        rbuffer = bytearray(8)
        i = 0
        
        if self.v < 2**(self.N)-1:
            struct.pack_into("B", rbuffer, i, self.v)
        else:            
            struct.pack_into("B", rbuffer, i, 2**(self.N)-1)
            i += 1
            self.v -= (2**(self.N)-1)

            while (self.v >= 128):
                struct.pack_into("B", rbuffer, i, (self.v % 128) + 128)
                i += 1
                self.v = round(self.v / 128)
                
                
            struct.pack_into("B", rbuffer, i, self.v)            
        
        return rbuffer     
        
    
    def decode(self, ibuffer):
        rval = 0
        i = 0
        m = 0
        next_octet = b''
        
        (rval,) = struct.unpack_from("B", ibuffer, i) 
        i += 1
        rval = rval  & (0xff - 2**(self.N))
        
        if rval < 2**(self.N)-1:
            return rval
        else:            
            (next_octet,) = struct.unpack_from("B", ibuffer, i)
            i += 1
            rval += ((next_octet & 127) * (2**m))
            m += 7
            
            while (next_octet & 128 == 128):
                (next_octet,) = struct.unpack_from("B", ibuffer, i)
                i += 1
                rval += ((next_octet & 127) * 2**m)
                m += 7
                
            return rval
    
class h2str:
    def __init__(self, initv=""):
        self.v = initv
    
    def encode(self, huffman=0x00): # or 0x01
        rbuffer = bytearray(1 + len(self.v))        
        strlen = h2int(initv=huffman + len(self.v), octet_offset=0)
        
        struct.pack_into("B", rbuffer, 0, strlen.encode()[0])
        
        if huffman > 0:
            pass # encode huffman
        else:            
            struct.pack_into("" + str(len(self.v)) + "s", rbuffer, 1, self.v.encode())
        
        return rbuffer
    
    def decode(self, ibuffer):
        (rlen,) = struct.unpack_from("B", ibuffer, 0)
        
        if (rlen & 0x80):
            pass # decode huffman
        else:
            return struct.unpack_from(str(rlen & 0x7f) + "s", ibuffer, 1)
    
    
class h2hf:
    def __init__(self, hname="", hval="", hindex=0):
        self.name_index = hindex # + dynamic offset
        self.name_literal = hname
        self.value_literal = hval
    
    
    # literal + indexing,       index = 0100 (0x2) + index | 0 (new_name)
    #    index(dynamic) + literal_name + literal_value
    # literal (no indexing),    index = 0000 + index | 0 (new_name)
    #    index(static) + literal_value
    # literal (protected),      index = 0001 (0x8) + index | 0 (new_name)
    #    literal_name + literal_value
    # indexed,                    index = 1 (0x1) + index
    #    index(static)
    
    
    def encode(self, htype):
        rbuffer = None
        hfindex = None
        hfname = None
        hfvalue = None
        
        if (htype == 0x01): # indexed
            rbuffer = bytearray(1)
            hfindex = h2int(initv=htype + self.name_index, octet_offset=0)            
                        
            struct.pack_into("B", rbuffer, 0, hfindex.encode()[0])           
            
            return rbuffer
        
        elif (htype == 0x02): # literal       
            rbuffer = bytearray(3 + len(self.value_literal) + len(self.name_literal))
            hfindex = h2int(initv=htype + self.name_index, octet_offset=0)
            hfvalue = h2str(initv=self.value_literal)
            hfname = h2str(initv=self.name_literal)            
            i = 0            
            
            struct.pack_into("B", rbuffer, 0, hfindex.encode()[0])
            i += 1
            struct.pack_into(str(len(hfname.encode())) + "s", rbuffer, i, hfname.encode())
            i += len(hfname.encode())
            struct.pack_into(str(len(hfvalue.encode())) + "s", rbuffer, i, hfvalue.encode())
            
            return rbuffer    
    
    def decode(self, ibuffer):
        hfindex = None
        hfname = None
        hfvalue = None
        i = 0
        
        (hfindex, ) = struct.unpack_from("B", ibuffer, i)
        i += struct.calcsize("B")
        # 0 1 2 3 4 5 6 7
        #B1 0 0 0 0 0 0 0
        #X1       0
        # but in spec examples, yields x80, WHY?      
        if (hfindex & 0x80):
            hfindex = hfindex - 0x01
            
            if hfindex > 0:
                hfname = field_static[hfindex][0]
                hfvalue = field_static[hfindex][1]
            
                return (hfname, hfvalue)
            else:
                pass # ERROR    
                
        elif (hfindex & 0x40):
            hfindex = hfindex - 0x02
            
            if hfindex > 0:                
                (dlen,) = struct.unpack_from("B", ibuffer, i)
                i += struct.calcsize("B")
                (hfname,) = struct.unpack_from(str(dlen & 0x7f) + "s", ibuffer, i)
                i += dlen & 0x7f
                (dlen,) = struct.unpack_from("B", ibuffer, i)
                i += struct.calcsize("B")
                (hfvalue,) = struct.unpack_from(str(dlen & 0x7f) + "s", ibuffer, i)
                
                return (hfname, hfvalue, hfindex)
        
class h2hpack:
    def __init__(self):
        self.field = [b'', b'']
        self.field_dyn = []     # compression dynamic header table
        self.header_list = []   # decoded header list
        self.header_block = b''
        self.protected_headers = [] # no compression headers
   
    
    
    
class _TestHPack:
    def __init__(self):
        pass
    
    def int_at(self, v, o):
        i = h2int(initv=v, octet_offset=o)
        
        for x in i.encode():
            if x == 0:
                break
            print(format(x, "0>8b"))
            
        print ("Decoded: " + str(i.decode(i.encode())))
            
    def hf(self, hname, hval, htype):        
        hf = h2hf(hname, hval, 62)
        
        print(hf.encode(htype).hex(sep=' ', bytes_per_sep=2))        
        print("Decoded: " + str(hf.decode(hf.encode(htype))))
        
        
test_hpack = _TestHPack()
test_hpack.int_at(1337, 3)
test_hpack.int_at(42, 0)
test_hpack.hf("custom-key", "custom-header", 0x02)
    