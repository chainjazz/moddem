'''
Created on 28 Apr 2020

@author: dkr85djo
'''

import xml.etree.ElementTree as ET

class MDGameStateXML:
    def __init__(self):
        self.diff_xml = None
        # build an XML stub for gamestate inline        
        self.xmlroot = ET.Element(
            'modealgame',
            attrib={
                'id':'MDXHRContainer',
                'active':'False'
                })
        self.xmlroot.append(ET.Element(
            'players',
            attrib={
                'id':'MDXHRPlayers'
                })
        )
    
    def gsupdate(self, gameon, drawpile, players):
        xml_player = None
        self.diff_xml = ET.fromstring(ET.tostring(self.xmlroot))
        xml_players = self.diff_xml.find('players')
        
        # update gameactive flag
        self.xmlroot.set('active', str(gameon))
        
        # rebuild gamestate xml from scratch (TODO: EXPENSIVE?)
        # NOTE: WE SHOULD ONLY PASS "DIRTY" PLAYERS, TODO, FIXME        
        for p in players: 
            xml_player = ET.Element(
                'player',
                attrib={'id':p.handle.decode(), 
                        'name':p.name.decode(),
                        'dirty':str(p.dirty)})   
            
            xml_hand = ET.Element('hand')                       
            xml_bank = ET.Element('bank')
            xml_prop = ET.Element('prop')
            
            for card in p.hand.cards:     # for each mem object card index
                xml_hand.append(ET.Element('card', 
                                           attrib={
                                               "cardid":str(card.cardid),
                                               "ctype":str(card.cardtype)})) # append
            for card in p.bank.cards:     # for each mem object card index
                xml_bank.append(ET.Element('card', 
                                           attrib={
                                               "cardid":str(card.cardid),
                                               "ctype":str(card.cardtype)})) # append
            for card in p.prop.cards:     # for each mem object card index
                xml_prop.append(ET.Element('card', 
                                           attrib={
                                               "cardid":str(card.cardid),
                                               "ctype":str(card.cardtype)})) # append
                
            xml_player.append(xml_hand)
            xml_player.append(xml_bank)
            xml_player.append(xml_prop)
            xml_players.append(xml_player)
            
            # TODO: what about drawpile?
            # (,,WHAT ABOOOOUT US!'')       
                
    def tostring(self, tailoredfor=None):
        # trick to make an element copy (via fromstring(tostring))
        # (we keep new_root in case we need to pass other data here)       
        new_root = ET.fromstring(ET.tostring(self.diff_xml))
                            
        if not (tailoredfor == None):
            # remove non-public elements for all but requesting client            
            new_root.set('whoami', tailoredfor.decode())
            
            for p in new_root.find('players').iter('player'):
                if not (p.get('id') == tailoredfor.decode()):
                    for h in p.iter('hand'):
                        p.remove(h)            
        
        return ET.tostring(new_root, 
                           encoding="utf-8", 
                           xml_declaration=True,
                           short_empty_elements=False)