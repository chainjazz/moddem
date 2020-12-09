'''
Created on 24 Apr 2020

@author: dkr85djo
'''


from random import randint

import modealdata as MDGS

from modealcard import MDCardCollection
from modealplayer import MDPlayer
from modealxml import MDGameStateXML


        
class MDGameState(MDGameStateXML):
    def __init__(self):
        self.gameon = None
        self.startRequest = None
        self.players = None     
        self.drawpile = None
        self.whichplayer = 0
        
        self.reset_game_state()       
    
    def induct_player(self, phandle, pname=None, pconn=None):
        playerExists = False
        
        for p in self.players:
            if p.handle == phandle:
                playerExists = True             
                
        if playerExists == False:
            self.players.append(MDPlayer(phandle, pname, pconn))                       
        else:
            return
        
        for p in self.players:
            p.dirty = True
            
        self.gsupdate(self.gameon, self.drawpile, self.players)        
            
    def reload_player(self, pcookie, newconn):
        for p in self.players:
            if pcookie == p.handle:                        
                if not (p.conn == newconn):
                    p.conn = newconn
        
    def deal_cards(self, p, n):
        if p.requestCards > 0:  # bullshit                      
            for i in range(n): # or 2?
                p.hand.add(self.drawpile.remove(
                    randint(0, self.drawpile.length() - 1)))        
            
            p.requestCards = 0
        
        p.dirty = True
        print(p.hand.cards, " (", p.handle, ")")           
            
    def set_game_state(self, gameon):
        self.gameon = gameon
        
        # state change only, not pertinent to drawing, no dirty flag
        
        
    def reset_game_state(self):
        super().__init__()
        self.gameon = False
        self.startRequest = False
        self.players = []     
        self.drawpile = MDCardCollection(0, False)
        self.whichplayer = 0
        
        # build deck 
        # TODO: Expensive
        self.drawpile.generate(MDGS.cardset)        
        # associate coloursets                      
        self.colourset = MDGS.colourset
        
        super().gsupdate(self.gameon, self.drawpile, self.players)
    def update_game_state(self):
        self.gsupdate(self.gameon, self.drawpile, self.players)
        
    def game_loop(self, ipc):    
        # Player assembly
        print("Entering assembly loop")
        
        super().gsupdate(self.gameon, self.drawpile, self.players)
        
        while ((len(self.players) < 5) and 
               (self.startRequest == False)): # indentation going AWOL here             
            ipc.daemon_openconn()
        
        # Start game
        self.set_game_state(True)
        
        # Initial deal        
        for p in self.players:
            self.deal_cards(p, 5) 
        
        # Select active player
        self.whichplayer = randint(0, len(self.players) - 1)
        
        # update gamestate
        super().gsupdate(self.gameon, self.drawpile, self.players)
        
              
            
        
        # Game loop  
        print("Entering game loop")      
        
        while (self.gameon == True):            
            ipc.daemon_openconn()        
        
        ipc.daemon_shutdown()



