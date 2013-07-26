import pygame
from numpy import random

#------------------------------
# A class for anything that needs to be displayed. I would have it in the main
# module, but it's a suprclass of Card, so Card needs to know about it.
# Simply defines an image and associated rectangle for an object.
class displayObject():
    def __init__(self, object_im, x=None, y=None):
        if type(object_im) == str:
            self.image = pygame.image.load('./images/'+object_im)
        else:
            self.image = object_im
        self.rect = self.image.get_rect()
        if x != None and y != None:
            self.rect.center = x, y

#------------------------------
# Classes for different types of cards

# Generic class for all cards. This is a subclass of displayObject and a
# superclass of all other card types.
# Just allocates a name, image and rectangle to a card.
class Card(displayObject):
    def __init__(self, card_im, name):
        displayObject.__init__(self, 'cards/'+card_im)
        self.name = name

# -----------------
# Character card
# Defines a player's character card as just a card with that character's name on
# it
class characterCard(Card):
    def __init__(self, charname):
        card_im = 'player cards/'+charname+'card.jpg'
        name = charname+' character card'
        Card.__init__(self, card_im, name)

# -----------------
# Hobbit card class
# Defines a Hobbit card as a card called 'hobbit card', with a value of one and
# a particular symbol and colour.
class hobbitCard(Card):
    def __init__(self, sym, col):
        self.symbol = sym
        self.colour = col
        self.value = 1
        self.stats = [self.colour, self.symbol]
        im = 'hobbit cards/'+col+'_'+sym+'.jpg'
        Card.__init__(self, im, 'hobbit card')
        self.isfrodojoker = False

# -----------------
# Feature card class
# Defines a feature card with symbol, colour, name and optional value (default
# is 1)
class featureCard(Card):
    def __init__(self, sym, col, name, val=1):
        self.symbol = sym
        self.colour = col
        self.value = val
        self.stats = [self.colour, self.symbol]
        cardname = name.split('/')[1]
        im = 'feature cards/'+name+'.jpg'
        Card.__init__(self, im, cardname)
        self.isfrodojoker = False

# -----------------
# Yellow card template.
# Defines card with name and colour. Symbol will be defined later as the
# description of each individual card's function.
class yellowCard(Card):
    def __init__ (self, name):
        self.symbol = None
        self.colour = 'yellow'
        im = 'feature cards/'+name+'.jpg'
        cardname = name.split('/')[1]
        Card.__init__(self, im, cardname)
        self.isfrodojoker = False
        self.icon = displayObject('cards/feature cards/'+name+'_icon.jpg')

#------------------------------
# Hobbit card deck.
# 60 Hobbit cards, which are shuffled and the first of which is removed when a player 'draws' it.

deck = []
discard_pile = []

hobbit1 = hobbitCard('joker', 'white')
deck.append(hobbit1)
hobbit2 = hobbitCard('joker', 'white')
deck.append(hobbit2)
hobbit3 = hobbitCard('joker', 'white')
deck.append(hobbit3)
hobbit4 = hobbitCard('joker', 'white')
deck.append(hobbit4)
hobbit5 = hobbitCard('joker', 'white')
deck.append(hobbit5)
hobbit6 = hobbitCard('joker', 'white')
deck.append(hobbit6)
hobbit7 = hobbitCard('joker', 'white')
deck.append(hobbit7)
hobbit8 = hobbitCard('joker', 'white')
deck.append(hobbit8)
hobbit9 = hobbitCard('joker', 'white')
deck.append(hobbit9)
hobbit10 = hobbitCard('joker', 'white')
deck.append(hobbit10)
hobbit11 = hobbitCard('joker', 'white')
deck.append(hobbit11)
hobbit12 = hobbitCard('joker', 'white')
deck.append(hobbit12)
hobbit13 = hobbitCard('fighting', 'white')
deck.append(hobbit13)
hobbit14 = hobbitCard('fighting', 'white')
deck.append(hobbit14)
hobbit15 = hobbitCard('fighting', 'white')
deck.append(hobbit15)
hobbit16 = hobbitCard('fighting', 'white')
deck.append(hobbit16)
hobbit17 = hobbitCard('fighting', 'white')
deck.append(hobbit17)
hobbit18 = hobbitCard('fighting', 'white')
deck.append(hobbit18)
hobbit19 = hobbitCard('fighting', 'white')
deck.append(hobbit19)
hobbit20 = hobbitCard('fighting', 'grey')
deck.append(hobbit20)
hobbit21 = hobbitCard('fighting', 'grey')
deck.append(hobbit21)
hobbit22 = hobbitCard('fighting', 'grey')
deck.append(hobbit22)
hobbit23 = hobbitCard('fighting', 'grey')
deck.append(hobbit23)
hobbit24 = hobbitCard('fighting', 'grey')
deck.append(hobbit24)
hobbit25 = hobbitCard('hiding', 'white')
deck.append(hobbit25)
hobbit26 = hobbitCard('hiding', 'white')
deck.append(hobbit26)
hobbit27 = hobbitCard('hiding', 'white')
deck.append(hobbit27)
hobbit28 = hobbitCard('hiding', 'white')
deck.append(hobbit28)
hobbit29 = hobbitCard('hiding', 'white')
deck.append(hobbit29)
hobbit30 = hobbitCard('hiding', 'white')
deck.append(hobbit30)
hobbit31 = hobbitCard('hiding', 'white')
deck.append(hobbit31)
hobbit32 = hobbitCard('hiding', 'grey')
deck.append(hobbit32)
hobbit33 = hobbitCard('hiding', 'grey')
deck.append(hobbit33)
hobbit34 = hobbitCard('hiding', 'grey')
deck.append(hobbit34)
hobbit35 = hobbitCard('hiding', 'grey')
deck.append(hobbit35)
hobbit36 = hobbitCard('hiding', 'grey')
deck.append(hobbit36)
hobbit37 = hobbitCard('travelling', 'white')
deck.append(hobbit37)
hobbit38 = hobbitCard('travelling', 'white')
deck.append(hobbit38)
hobbit39 = hobbitCard('travelling', 'white')
deck.append(hobbit39)
hobbit40 = hobbitCard('travelling', 'white')
deck.append(hobbit40)
hobbit41 = hobbitCard('travelling', 'white')
deck.append(hobbit41)
hobbit42 = hobbitCard('travelling', 'white')
deck.append(hobbit42)
hobbit43 = hobbitCard('travelling', 'white')
deck.append(hobbit43)
hobbit44 = hobbitCard('travelling', 'grey')
deck.append(hobbit44)
hobbit45 = hobbitCard('travelling', 'grey')
deck.append(hobbit45)
hobbit46 = hobbitCard('travelling', 'grey')
deck.append(hobbit46)
hobbit47 = hobbitCard('travelling', 'grey')
deck.append(hobbit47)
hobbit48 = hobbitCard('travelling', 'grey')
deck.append(hobbit48)
hobbit49 = hobbitCard('friendship', 'white')
deck.append(hobbit49)
hobbit50 = hobbitCard('friendship', 'white')
deck.append(hobbit50)
hobbit51 = hobbitCard('friendship', 'white')
deck.append(hobbit51)
hobbit52 = hobbitCard('friendship', 'white')
deck.append(hobbit52)
hobbit53 = hobbitCard('friendship', 'white')
deck.append(hobbit53)
hobbit54 = hobbitCard('friendship', 'white')
deck.append(hobbit54)
hobbit55 = hobbitCard('friendship', 'white')
deck.append(hobbit55)
hobbit56 = hobbitCard('friendship', 'grey')
deck.append(hobbit56)
hobbit57 = hobbitCard('friendship', 'grey')
deck.append(hobbit57)
hobbit58 = hobbitCard('friendship', 'grey')
deck.append(hobbit58)
hobbit59 = hobbitCard('friendship', 'grey')
deck.append(hobbit59)
hobbit60 = hobbitCard('friendship', 'grey')
deck.append(hobbit60)

#------------------------------
# Yellow cards
# Defines the yellow cards.

# Athelas.
athelas = yellowCard('rivendell/Athelas')
athelas.symbol = 'One player: Ignore any effects of missing Life tokens once only'
athelas.stats = [athelas.symbol]
# Miruvor.
miruvor = yellowCard('rivendell/Miruvor')
miruvor.symbol = 'One player: May pass 1 card to another player'
miruvor.stats = [miruvor.symbol]
# Mithril.
mithril = yellowCard('rivendell/Mithril')
mithril.symbol = 'One player: Ignore effects after one die roll'
mithril.stats = [mithril.symbol]
# Staff.
staff = yellowCard('rivendell/Staff')
staff.symbol = 'Ignore one tile showing a sundial and three items'
staff.stats = [staff.symbol]
# Belt.
belt = yellowCard('lothlorien/Belt')
belt.symbol = 'One player: Do not roll one die'
belt.stats = [belt.symbol]
# Elessar.
elessar = yellowCard('lothlorien/Elessar')
elessar.symbol = 'One player: [whitecircle]'
elessar.stats = [elessar.symbol]
# Lembas.
lembas = yellowCard('lothlorien/Lembas')
lembas.symbol = 'One player: Draw Hobbit cards to increase hand to 6 cards'
lembas.stats = [lembas.symbol]
# Phial.
phial = yellowCard('lothlorien/Phial')
phial.symbol = 'Active player: Do not reveal the next tile'
phial.stats = [phial.symbol]

# --------------------
# Rivendell feature cards.
# Function puts the Rivendell feature cards into a random order to be dealt out.
def shuffle_rivendell():
    r = []
    riv = 'rivendell/'
    gandalf = featureCard('travelling', 'white', riv+'Gandalf', 2)
    r.append(gandalf)
    glamdring = featureCard('joker', 'grey', riv+'Glamdring', 2)
    r.append(glamdring)
    aragorn = featureCard('joker', 'white', riv+'Aragorn', 2)
    r.append(aragorn)
    anduril = featureCard('fighting', 'grey', riv+'Anduril', 2)
    r.append(anduril)
    gimli = featureCard('fighting', 'white', riv+'Gimli', 2)
    r.append(gimli)
    legolas = featureCard('hiding', 'white', riv+'Legolas', 2)
    r.append(legolas)
    boromir = featureCard('fighting', 'white', riv+'Boromir', 2)
    r.append(boromir)
    sting = featureCard('joker', 'grey', riv+'Sting')
    r.append(sting)
    r.append(miruvor)   # Miruvor
    r.append(mithril)   # Mithril
    r.append(staff)     # Staff
    r.append(athelas)   # Athelas

    random.shuffle(r)
    return r

# --------------------
# Moria feature cards.
book = featureCard('hiding', 'grey', 'moria/Book')
pipe = featureCard('friendship', 'grey', 'moria/Pipe', 2)

# --------------------
# Lothlorien feature cards
# Same as shuffle_rivendell() but for Lothlorien
def shuffle_loth():
    l = []
    loth = 'lothlorien/'
    arwen = featureCard('joker', 'grey', loth+'Arwen', 2)
    l.append(arwen)
    box = featureCard('joker', 'grey', loth+'Box of Earth', 1)
    l.append(box)
    rope = featureCard('travelling', 'grey', loth+'Elven Rope', 2)
    l.append(rope)
    galadriel = featureCard('joker', 'grey', loth+'Galadriel', 2)
    l.append(galadriel)
    brooch = featureCard('friendship', 'grey', loth+'Brooch', 1)
    l.append(brooch)
    bow = featureCard('friendship', 'grey', loth+'Bow', 1)
    l.append(bow)
    boat = featureCard('travelling', 'grey', loth+'Boat', 1)
    l.append(boat)
    cloak = featureCard('hiding', 'grey', loth+'Elven Cloak', 2)
    l.append(cloak)
    l.append(belt)
    l.append(phial)
    l.append(lembas)
    l.append(elessar)

    random.shuffle(l)
    return l

# --------------------
# Activity line cards.
linecards = [book]#, theoden, shadowfax, eomer, faramir, army, ghan, eowyn]
