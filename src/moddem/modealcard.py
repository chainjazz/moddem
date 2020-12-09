'''
Created on 11 Apr 2020

@author: dkr85djo
'''

class md:
    MAXCARDS = 106
    
class MDColourSet:    
    def __init__(self, value, names, hexcolour=b'#000000'):
        self.value = value
        self.names = names        
        self.hexcolour = hexcolour
        
    def size(self):
        return len(self.names)   
    
class MDCard: # ABSTRACT    
    def __init__(self, value, titleid, cardid=0, ctype=0):
        self.value = value      # monetary value: may be index or literal (direct)
        self.title = titleid    # descriptive text: index
        self.cardid = cardid    # explicit index, direct, implicit, set by drawpile generator
        self.cardtype = ctype   # card type: implicit, set by derived constructors
        
class MDMoneyCard(MDCard):
    def __init__(self, value, titleid, inctype=4, colourset=None):
        MDCard.__init__(self, value, titleid, ctype=inctype)
        self.cardtype = inctype
        self.colourset = colourset
        
class MDPropertyCard(MDCard):
    def __init__(self, value, titleid, colourset=None, inctype=0):
        MDCard.__init__(self, value, titleid, ctype=inctype)
        self.colourset = colourset # if non wild card, 1 element
        self.cardtype = inctype + min(len(colourset) - 1, 1)

# targetall = True => whichtarget=all
# targetall = False => whichtarget=$var (one of which is 'self')
        
class MDActionCard(MDCard):   
    def __init__(self, value, titleid, colourset=None, targetall=False, inctype=2):
        MDCard.__init__(self, value, titleid, ctype=inctype)
        self.targetall = targetall
        self.colourset = colourset
        self.cardtype = inctype + min(len(colourset) - 1, 1)

class MDCardCollection:    
    def __init__(self, ownerid, ispublic=False):
        self.ownerid = ownerid
        self.ispublic = ispublic
        self.cards = []            
    
    def generate(self, cardset):
        for i in range(len(cardset)):
            newcardobject = cardset[i]
            newcardobject.cardid = i # need to generate cardid here
            self.cards.append(newcardobject) # we are agnostic to the type of card
       
    def length(self): # FIXME: We should just use len()
        return (len(self.cards))
            
    def remove(self, index):
        return self.cards.pop(index)          
    
    def add(self, cardobject):
        self.cards.append(cardobject)    
        





