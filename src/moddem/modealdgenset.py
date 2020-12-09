'''
Created on 20 Apr 2020

@author: dkr85djo
'''

import xml.etree.ElementTree as ET

from modealcard import MDColourSet, MDCard, MDMoneyCard, MDActionCard, MDPropertyCard 

class MDOriginSet:
    def __init__(self, colourset, cardset):
        self.colourset = colourset
        self.originset = cardset
        
    def serialize_xml(self):
        cardid = 0
        csetid = 0
        md_origin = ET.parse('mdorigin.xml')
        xml_origin = md_origin.getroot()
        xml_origincset = ET.Element("coloursets")
        xml_originset = ET.Element("cards")        
        
        for citem in self.colourset:
            if isinstance(citem, MDColourSet):
                xml_cset = ET.Element(
                    'cset',
                    attrib={
                        'csetid':str(csetid), # counter, see below
                        'value':str(citem.value),
                        'hex':str(citem.hexcolour)
                        }
                    )
                for csprop in citem.names:
                    xml_cspname = ET.Element('name')
                    xml_cspname.text = csprop
                    xml_cset.append(xml_cspname)
                
            xml_origincset.append(xml_cset)
            csetid += 1
                
        for citem in self.originset:
            if isinstance(citem, MDCard):
                xml_card = ET.Element(
                        'card',
                        attrib={
                            'value':str(citem.value),
                            'title':citem.title,
                            'cardid':str(cardid),                           
                            'ctype':str(citem.cardtype)                            
                        }
                )
                
            if isinstance(citem, (MDMoneyCard, MDPropertyCard, MDActionCard)):
                for cs in citem.colourset:
                    cset = ET.Element('cset')
                    cset.text = str(cs)
                    xml_card.append(cset)
            
            if isinstance(citem, MDActionCard):
                xml_card.set('targetall', str(citem.targetall))
            
            xml_originset.append(xml_card)            
            cardid += 1
        
        xml_origin.append(xml_origincset)
        xml_origin.append(xml_originset)
        md_origin.write('mdoriginset.xml')
          

         
        
    
        

