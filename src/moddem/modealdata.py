'''
Created on 28 Apr 2020

@author: dkr85djo
'''

from modealcard import MDColourSet, MDCard, MDMoneyCard, MDActionCard, MDPropertyCard 

colourset = [
    MDColourSet(1, ["Whitechapel Road", 
                    "Old Kent Road",
                    '', # alignment padding element
                    '',
                    'Rent' # constant index for Rent cards (or Wild Cards)
                    'Wild Card'], hexcolour="#331100"),      # brown 0
    
    MDColourSet(1, ["Electric Company",
                    "Water Works",
                    '',
                    '',
                    'Rent'
                    'Wild Card'], hexcolour="#bbffbb"),        # util 1 
    MDColourSet(1, ["The Angel Islington", 
                    "Pentonville Road", 
                    "Euston Road",
                    '',
                    'Rent'
                    'Wild Card'], hexcolour="#bbffff"),        # cyan 2
    MDColourSet(1, ["Kings Cross St.",
                    "Fenchurch St.",
                    "Liverpool St. St.",
                    "Marylebone St.",
                    'Rent'
                    'Wild Card'], hexcolour="#111111"),     # stat 3
    MDColourSet(2, ["Pall Mall",
                    "Northumberland",
                    "Whitehall",
                    '',
                    'Rent'
                    'Wild Card'], hexcolour="#ff00ff"),          # pink 4
    MDColourSet(2, ["Bow Street",
                    "Vine Street",
                    "Marlborough St.",
                    '',
                    'Rent'
                    'Wild Card'], hexcolour="#ffaa00"),    # orange 5
    MDColourSet(3, ["Fleet Street",
                    "Strand",
                    "Trafalgar Sq.",
                    '',
                    'Rent'
                    'Wild Card'], hexcolour="#ff0000"),      # red 6
    MDColourSet(3, ["Piccadilly",
                    "Leicester",
                    "Coventry St.",
                    '',
                    'Rent'
                    'Wild Card'], hexcolour="#ffff00"),       # yellow 7
    MDColourSet(4, ["Park Lane",
                    "Mayfair",
                    '',
                    '',
                    'Rent'
                    'Wild Card'], hexcolour="#2222ff"),            # blue 8
    MDColourSet(4, ["Regent Street",
                    "Bond Street",
                    "Oxford Street",
                    '',
                    'Rent'
                    'Wild Card'], hexcolour="#22ff22"),      # green 9
    
    # META COLOUR SETS
    MDColourSet( # INDEX 10, DEPENDENT MDActionCard
        0,              # ignored-override
        ['Double Rent',
         'Pass Go',
         'Birthday',
         'House',
         'Debt Collector',
         'Forced Deal',
         'Sly Deal',
         'Hotel',
         'NO!',
         'DEAL BREAKER'
         ],
        hexcolour=None  # ignored
        ),
    
    MDColourSet( # INDEX 11, DEPENDEND MDMoneyCard
        0, # ignored-override
        ['1m',
         '2m',
         '3m',
         '4m',
         '5m',
         '10m'
         ],
        hexcolour=None                 
        )
    
    
]

colourvalueset = [
        
    ]


#     cardtype is set implicitly by constructors
#     and subject to colourset length (except for money)
cardset = [ # THIS SHIT SHOULD BE IN DATABASE
    
    MDMoneyCard(1,  0, colourset=[11]),
    MDMoneyCard(1,  0, colourset=[11]),
    MDMoneyCard(1,  0, colourset=[11]),
    MDMoneyCard(1,  0, colourset=[11]),
    MDMoneyCard(1,  0, colourset=[11]),
    MDMoneyCard(1,  0, colourset=[11]),
    MDMoneyCard(2,  1, colourset=[11]),
    MDMoneyCard(2,  1, colourset=[11]),
    MDMoneyCard(2,  1, colourset=[11]),
    MDMoneyCard(2,  1, colourset=[11]),
    MDMoneyCard(2,  1, colourset=[11]),
    MDMoneyCard(3,  2, colourset=[11]),
    MDMoneyCard(3,  2, colourset=[11]),
    MDMoneyCard(3,  2, colourset=[11]),
    MDMoneyCard(4,  3, colourset=[11]),
    MDMoneyCard(4,  3, colourset=[11]),
    MDMoneyCard(4,  3, colourset=[11]),
    MDMoneyCard(5,  4, colourset=[11]),
    MDMoneyCard(5,  4, colourset=[11]),
    MDMoneyCard(10, 5, colourset=[11]),

    # ActionActions
    MDActionCard(1, 0, colourset=[10]),
    MDActionCard(1, 0, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(1, 1, colourset=[10]),
    MDActionCard(2, 2, colourset=[10],targetall=True),
    MDActionCard(2, 2, colourset=[10], targetall=True),
    MDActionCard(2, 2, colourset=[10], targetall=True),
    MDActionCard(3, 3, colourset=[10]),
    MDActionCard(3, 3, colourset=[10]),
    MDActionCard(3, 3, colourset=[10]),
    MDActionCard(3, 4, colourset=[10]),
    MDActionCard(3, 4, colourset=[10]),
    MDActionCard(3, 4, colourset=[10]),
    MDActionCard(3, 5, colourset=[10]),
    MDActionCard(3, 5, colourset=[10]),
    MDActionCard(3, 5, colourset=[10]),
    MDActionCard(3, 6, colourset=[10]),
    MDActionCard(3, 6, colourset=[10]),
    MDActionCard(3, 6, colourset=[10]),
    MDActionCard(4, 7, colourset=[10]),
    MDActionCard(4, 7, colourset=[10]),
    MDActionCard(4, 8, colourset=[10], targetall=True),
    MDActionCard(4, 8, colourset=[10], targetall=True),
    MDActionCard(4, 8, colourset=[10], targetall=True),
    MDActionCard(5, 9, colourset=[10]),
    MDActionCard(5, 9, colourset=[10]),
    # ActionRents
    MDActionCard(1, 4, colourset=[0,2], targetall=True),
    MDActionCard(1, 4, colourset=[0,2], targetall=True),
    MDActionCard(1, 4, colourset=[4,5], targetall=True),
    MDActionCard(1, 4, colourset=[4,5], targetall=True),
    MDActionCard(1, 4, colourset=[1,3], targetall=True),
    MDActionCard(1, 4, colourset=[1,3], targetall=True),
    MDActionCard(1, 4, colourset=[6,7], targetall=True),
    MDActionCard(1, 4, colourset=[6,7], targetall=True),
    MDActionCard(1, 4, colourset=[8,9], targetall=True),
    MDActionCard(1, 4, colourset=[8,9], targetall=True),
    MDActionCard(3, 4, colourset=[0,1,2,3,4,5,6,7,8,9]),
    MDActionCard(3, 4, colourset=[0,1,2,3,4,5,6,7,8,9]),
    MDActionCard(3, 4, colourset=[0,1,2,3,4,5,6,7,8,9]),

    # PropertyCards
    MDPropertyCard(colourset[0].value, 0, colourset=[0]), #brown
    MDPropertyCard(colourset[0].value, 1, colourset=[0]), #brown
    MDPropertyCard(colourset[1].value, 0, colourset=[1]), #util
    MDPropertyCard(colourset[1].value, 1, colourset=[1]), #util
    MDPropertyCard(colourset[2].value, 0, colourset=[2]), #cyan
    MDPropertyCard(colourset[2].value, 1, colourset=[2]), #cyan
    MDPropertyCard(colourset[2].value, 2, colourset=[2]), #cyan
    MDPropertyCard(colourset[3].value, 0, colourset=[3]), #stat
    MDPropertyCard(colourset[3].value, 1, colourset=[3]), #stat
    MDPropertyCard(colourset[3].value, 2, colourset=[3]), #stat
    MDPropertyCard(colourset[3].value, 3, colourset=[3]), #stat
    MDPropertyCard(colourset[4].value, 0, colourset=[4]), #pink
    MDPropertyCard(colourset[4].value, 1, colourset=[4]), #pink
    MDPropertyCard(colourset[4].value, 2, colourset=[4]), #pink
    MDPropertyCard(colourset[5].value, 0, colourset=[5]), #orange
    MDPropertyCard(colourset[5].value, 1, colourset=[5]), #orange
    MDPropertyCard(colourset[5].value, 2, colourset=[5]), #orange
    MDPropertyCard(colourset[6].value, 0, colourset=[6]), #red
    MDPropertyCard(colourset[6].value, 1, colourset=[6]), #red
    MDPropertyCard(colourset[6].value, 2, colourset=[6]), #red
    MDPropertyCard(colourset[7].value, 0, colourset=[7]), #yellow
    MDPropertyCard(colourset[7].value, 1, colourset=[7]), #yellow
    MDPropertyCard(colourset[7].value, 2, colourset=[7]), #yellow
    MDPropertyCard(colourset[8].value, 0, colourset=[8]), #blue
    MDPropertyCard(colourset[8].value, 1, colourset=[8]), #blue
    MDPropertyCard(colourset[9].value, 0, colourset=[9]), #green
    MDPropertyCard(colourset[9].value, 1, colourset=[9]), #green
    MDPropertyCard(colourset[9].value, 2, colourset=[9]), #green
    
    # Property Wild Cards
    MDPropertyCard(0, 5, colourset=[0,1,2,3,4,5,6,7,8,9]),
    MDPropertyCard(0, 5, colourset=[0,1,2,3,4,5,6,7,8,9]),
    MDPropertyCard(1, 5, colourset=[0,2]),
    MDPropertyCard(2, 5, colourset=[1,3]),
    MDPropertyCard(2, 5, colourset=[4,5]),
    MDPropertyCard(2, 5, colourset=[4,5]),
    MDPropertyCard(3, 5, colourset=[6,7]),
    MDPropertyCard(3, 5, colourset=[6,7]),
    MDPropertyCard(4, 5, colourset=[2,3]),
    MDPropertyCard(4, 5, colourset=[3,8]),
    MDPropertyCard(4, 5, colourset=[8,9])  
        
]