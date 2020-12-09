'''
Created on 24 Apr 2020

@author: dkr85djo
'''
from modealcard import MDCardCollection

class MDPropertyCollection(MDCardCollection):
    def __init__(self, ownerid, ispublic=True):
        MDCardCollection.__init__(self, ownerid, ispublic)        

class MDHand(MDCardCollection):
    def __init__(self, ownerid, ispublic=False):
        MDCardCollection.__init__(self, ownerid, ispublic)

class MDBankPile(MDCardCollection):
    def __init__(self, ownerid, ispublic=True):
        MDCardCollection.__init__(self, ownerid, ispublic)
        
class MDPlayer:   
    def __init__(self, phandle, pname=None, pconn=None):
        self.bank = MDBankPile(True)
        self.hand = MDHand(False)
        self.prop = MDPropertyCollection(True)
        self.disc = MDCardCollection(True) # discard pile buffer
        self.requestCards = 5               # how many cards to draw on turn or draw
        self.saynoCards = 0
        self.requestAllow = True # allow requests from others by default
        self.dirty = False # client redraw flag, not a dirty or stinky player
        # net stuff
        self.handle = phandle
        self.name = pname or phandle
        self.conn = pconn
            
    # implements interface Action
    def send_request(self, phandles, takeid, giveid, amount):
        for p in phandles:
            p.process_request([self.handle], takeid, giveid, amount)
    def process_request(self, phandles, takeid, giveid, amount):
        pass       
    def charge(self, handid, phandles, amount):        
        self.disc.add(self.hand.remove(handid))
    def prop_take(self, phandles, takeid):
        if phandles[0].requestAllow:
            self.prop.add(phandles[0].prop.remove(takeid))
    def prop_swap(self, phandles, takeid, giveid):
        if phandles[0].requestAllow:
            self.prop.add(phandles[0].prop.remove(takeid))
            phandles[0].prop.add(self.prop.remove(giveid))
    def sayno(self, handid):
        if self.saynoCards > 0:
            self.disc.add(self.hand.remove(handid))
            self.saynoCards = self.saynoCards - 1
            self.requestAllow = False        
    def prop_takeset(self, handid, phandles, cardids):
        self.disc.add(self.hand.remove(handid))
        
        if phandles[0].requestAllow:           
            for setcard in cardids:
                self.prop.add(phandles[0].prop.remove(setcard))
    def passgo(self, handid):
        self.disc.add(self.hand.remove(handid))
        self.draw(2)        
    def prop(self, handid):
        self.prop.add(self.hand.remove(handid))
    def bank(self, handid):
        self.bank.add(self.hand.remove(handid))
    def draw(self, amount):
        self.requestCards = amount