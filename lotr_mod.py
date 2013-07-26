from deck import *

#------------------------------
# Character template and useful character-based functions.
class Hobbit():
    def __init__(self, charname, colour):
        self.name = charname
        self.figure = displayObject(pygame.Surface((20,10)))
        self.displaycolour = colour
        self.figure.rect = self.figure.image.fill(colour)
        self.figure.player = self
        self.hand = []
        self.shields = 4
        self.tokens = [0, 0, 0] # List of tokens in order: Rings, hearts, suns.
        self.corr = 0
        self.ring = False
        self.active = False
        self.figure.rect.centerx = master.rect.left + 35
        self.char_card = characterCard(charname)
        self.powerblurb = None
        self.icon = displayObject('cards/player cards/'+charname+'_icon.jpg')
        self.icon.player = self

    def increase_corruption(self, spaces=1):
        if spaces < 0:
            if self.corr < abs(spaces):
                print_scr(['You cannot move that many spaces backwards on the '+
                    'corruption line.'])
                wait(1000)
                spaces = 0-self.corr
            for i in range(abs(spaces)):
                wait(500)
                self.corr -= 1
                self.figure.rect.centerx -= 35
                old_col = self.displaycolour
                new_col = [col-(self.corr*(col/24.)) for col in old_col]
                self.figure.image.fill(new_col)
                update_screen()
            text1 = self.name+' has moved '+str(abs(spaces))+ \
                ' spaces towards the light on the corruption line.'
            text2 = self.name+' is on space number '+str(self.corr)+'.'
            print_scr([text1, text2], 1000)
        elif spaces > 0:
            for i in range(spaces):
                wait(500)
                # Places player one step further along the corruption line.
                self.corr += 1
                self.figure.rect.centerx += 35
                old_col = self.displaycolour
                new_col = [col-(self.corr*(col/32)) for col in old_col]
                self.figure.image.fill(new_col)
                update_screen()
                # Points out your death should a Hobbit and Sauron share a space on the corruption line.
                if self.corr >= sau.corr:
                    #c = char_death(char)
                    #if c == 'next player':
                    #    a = a + 1
                    #    if a > len(players)-1:
                    #        a = 0
                    #    active_player = players[a]
                    #break
                    print "bummer"
            text1 = self.name+' has moved '+str(spaces)+' spaces towards the darkness on the corruption line.'
            text2 = self.name+' is on space number '+str(self.corr)+'.'
            print_scr([text1, text2], 1000)

# -----------------
# Class for Sauron
class dark_lord():
    def __init__(self):
        self.name = "Sauron"
        self.corr = 15
        self.figure = displayObject(pygame.Surface((20,10)))
        self.figure.rect = self.figure.image.fill((0,0,0))
        self.figure.rect.centerx = master.rect.left + 565
        self.figure.rect.top = 155

    def move_sauron(self, spaces=1):
        for i in range(spaces):
            pygame.time.delay(500)
            self.corr -= 1
            self.figure.rect.centerx -= 35
            update_screen()
        spaces = str(spaces)
        text1 = 'Sauron has moved '+spaces+' spaces towards you on the corruption line.'
        text2 = 'Sauron is on space number '+str(self.corr)
        print_scr([text1, text2], 1000)
        for p in players:
            if self.corr <= p.corr:
                #c = char_death(i)
                #if c == 'next player':
                #    a = a + 1
                #    if a > len(players)-1:
                #        a = 0
                #    active_player = players[a]
                print "Bummer."

# -----------------
# Define class for board markers
class marker(displayObject):
    def __init__(self, places):
        displayObject.__init__(self, 'marker.bmp')
        self.pos = 0
        self.places = places
    def move(self, scene=None):
        self.pos += 1
        update_screen(scene)

# -----------------
# Define class for the master board
class masterBoard():
    def __init__(self):
        self.surf = pygame.Surface((600, 200))
        self.image = pygame.image.load("./images/master.jpg")
        self.rect = self.surf.blit(self.image, (0,0))
        self.rect.centerx = screen_size[0]/2
        left, top = self.rect.topleft
        self.marker = marker([(left+25,top+55),(left+140,top+50),
            (left+235,top+10),(left+320,top+10),(left+400,top+55),
            (left+480,top+10),(left+550,top+30)])

    def move_marker(self):
        self.marker.pos += 1
        update_screen()
        """
        self.surf.blit(self.image, (0,0))
        screen.blit(self.surf, self.rect)
        screen.blit(self.marker.image, self.marker.places[self.marker.pos])
        pygame.display.update(self.rect)
        """

# -----------------
# Define class for boards
class scenarioBoard():
    def __init__(self, board_im):
        self.surf = pygame.Surface((600, 300))
        self.image = pygame.image.load("./images/"+board_im+".jpg")
        self.rect = self.surf.blit(self.image, (0,0))
        self.rect.topleft = x, y = master.rect.bottomleft
        left = x + 5
        self.event_marker = marker([(left,y-30), (left,y+15), (left,y+55), 
                                (left,y+105), (left,y+150), (left,y+185),
                                (left,y+220)])

    def move_marker(self):
        self.event_marker.pos += 1
        update_screen()

# -----------------
# Class for event tiles.
class event_tile(displayObject):
    def __init__ (self, name, move, desc, tile_type, im_name):
        displayObject.__init__(self, 'tiles/'+im_name)
        self.rect.midtop = (100, 360)
        self.name = name
        self.move = move
        self.description = desc
        self.tile_type = tile_type

# --------------------
# Activity line template.
class actline:
    def __init__(self, scene, linename):
        self.name = linename
        self.pos = 0
        self.readfile = open(scene + '/' + linename + '.dat', 'r')
        self.end = None
        self.marker = None

# -----------------
# Scenario template.
class scenario:
    def __init__(self, scenename, events_list):
        self.board = scenarioBoard(scenename)
        self.name = scenename
        self.event = 0
        self.events = events_list
        self.finished_lines = []
        self.features = True
        
        self.fighting = actline(scenename, 'fighting')
        self.hiding = actline(scenename, 'hiding')
        self.travelling = actline(scenename, 'travelling')
        self.friendship = actline(scenename, 'friendship')
        
        x, y = master.rect.bottomleft
        if scenename == 'Moria':
            self.fighting.marker = marker([(x+190,y+155),(x+225,y+140),
                (x+260,y+145),(x+290,y+155),(x+325,y+170),(x+360,y+175),
                (x+395,y+175),(x+430,y+170),(x+460,y+140),(x+470,y+100),
                (x+475,y+65)])
            self.hiding.marker = marker([(x+120,y+230),(x+145,y+230),
                (x+170,y+230),(x+195,y+230),(x+220,y+230),(x+245,y+230),
                (x+270,y+230),(x+295,y+230)])
            self.travelling.marker = marker([(x+380,y+230),(x+405,y+230),
                (x+430,y+230),(x+455,y+230),(x+480,y+230),(x+505,y+230),
                (x+530,y+230),(x+555,y+230)])
            self.lines = [self.fighting, self.hiding, self.travelling]
            lines_end = [20, 7, 7]
            self.noline = 'friendship'
            self.main_start = 10
        elif scenename == "Helm's Deep":
            self.lines = [self.fighting, self.friendship, self.travelling]
            lines_end = [40, 7, 10]
            self.noline = 'hiding'
            self.main_start = 30
        elif scenename == "Shelob's Lair":
            self.lines = [self.fighting, self.hiding, self.travelling]
            lines_end = [50, 7, 10]
            self.noline = 'friendship'
            self.main_start = 40
        elif scenename == 'Mordor':
            self.lines = [self.travelling, self.friendship, self.fighting, self.hiding]
            lines_end = [60, 7, 7, 7]
            self.noline = None
            self.main_start = 50

        self.main = self.lines[0]
        for l, line in enumerate(self.lines):
            line.end = lines_end[l]
        self.show_tiles = [event_tile('fighting', self.fighting, 
                            'Move the fighting line one space', 'activity', 
                            'fighting.jpg'),
                           event_tile('hiding', self.hiding, 
                            'Move the hiding line one space', 'activity', 
                            'hiding.jpg'), 
                           event_tile('travelling', self.travelling, 
                            'Move the travelling line one space.', 'activity', 
                            'travelling.jpg'),
                           event_tile('friendship', self.friendship,
                            'Move the friendship line one space', 'activity', 
                            'friendship.jpg')]
        for tile in self.show_tiles:
            if tile.name == self.noline:
                self.show_tiles.remove(tile)

# -----------------
# Generic loop for getting user input.
def standard_loop(buttons):
    while 1:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(pos):
                        if event.button == 3:
                            return button, True
                        else:
                            return button, False

# -----------------
# 
def choose_button(char, extra_buttons):
    buttons = extra_buttons + current_options
    while 1:
        for button in buttons:
            screen.blit(button.image, button.rect)
        update_screen()
        selected, right_click = standard_loop(buttons)
        if selected == ring_button:
            if ring_bearer.ring != True:
                print_scr(['The Ring-bearer must [blacksquare]'])
                r = dice(ring_bearer, scenario)
                ring(r, scenario)
                ring_bearer.ring = True
                current_options.remove(ring_button)
                if scenario.main.pos >= scenario.main.end:
                    return 'end'
            else:
                print_scr(['The Ring-bearer is already wearing the Ring',
                           'It will be removed at the end of the current scenario'])
            #return 'more tiles'
        elif selected == gandalf_button:
            call_gandalf()
            #return 'more tiles'
        #elif selected == hobbit_button:
        #    draw_hobbit_card(char, 2)
        elif selected in player_icons:
            show_player_stats(selected.player)
        #elif selected in player_figs:
        #    selected.player.increase_corruption(-1)
        elif selected in yellow_icons:
            print_scr(['Yellow cards are currently under development',
                       'Try again later'], 1500)
        elif selected in extra_buttons:
            return selected
        #screen.fill((0,0,0))

# -----------------
# Function to display information about a selected player
def show_player_stats(char):
    stats = char.tokens + [char.shields, len(char.hand)]
    colours = [(0,0,0), (0,0,0), (0,0,0), (255,255,255),(255,255,255)]
    font = pygame.font.Font(None, 36)
    width = screen_size[0] - master.rect.right
    surf = pygame.Surface((width, 300))
    rect = surf.fill(char.displaycolour)
    rect.bottomleft = master.rect.right, char.icon.rect.bottom
    for i, icon in enumerate(icons):
        surf.blit(icon.image, icon.rect)
        number = font.render(str(stats[i]), 1, colours[i])#(0,0,0))
        numrect = number.get_rect(center=icon.rect.center)
        surf.blit(number, numrect)
    
    screen.blit(surf, rect)
    pygame.display.update(rect)

# -----------------
# Function to choose the number of players.
def choose_num_players():
    num = 2
    cardback = pygame.image.load('./images/cards/player cards/plcard_back.jpg')
    print_scr(['Choose how many hobbits to play with',
               '(Right-click for character details).'])
    while 1:
        pos = pygame.mouse.get_pos()
        for p, player in enumerate(players):
            if player.char_card.rect.collidepoint(pos):
                num = p + 1
                if num < 2:
                    num = 2
        for p, player in enumerate(players):
            card = player.char_card
            if p < num:
                screen.blit(card.image, card.rect)
            else:
                screen.blit(cardback, card.rect)
        update_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for player in players:
                    if player.char_card.rect.collidepoint(pos):
                        selected = player
                        if event.button == 3:
                            text = player.name+': '+player.powerblurb
                            print_scr([text])
                        else:
                            screen.fill((0,0,0))
                            print_scr(['Beginning a '+str(num)+'-player game.'])
                            return num

# -------------------
# Function to return a player chosen from the screen
def choose_player(choose_from_plrs, displayitem=None, scene=None):
    x = 0
    sep = screen_size[0]/(len(choose_from_plrs)+1)
    for player in choose_from_plrs:
        x += sep
        player.char_card.rect.centerx = x
        screen.blit(player.char_card.image, player.char_card.rect)
    update_screen()
    if displayitem != None:
        displayitem.rect.centerx = master.rect.centerx
        displayitem.rect.bottom = master.rect.height - 25
        screen.blit(displayitem.image, displayitem.rect)
        pygame.display.update(displayitem.rect)
    buttons = [player.char_card for player in choose_from_plrs]
    buttons.append(displayitem)
    bdict = dict(zip(buttons, choose_from_plrs))
    looping = True
    while looping:
        selected, right_click = standard_loop(buttons)
        try:
            player = bdict[selected]
        except KeyError:
            player = None
        if not right_click:
            looping = False
        elif player != None:
            show_hand(player, player.hand, False, scene)
            screen.fill((0,0,0))
            print_scr([''])
            for player in choose_from_plrs:
                pl_card = player.char_card
                screen.blit(pl_card.image, pl_card.rect)
            update_screen()
            if displayitem != None:
                screen.blit(displayitem.image, displayitem.rect)
                pygame.display.update(displayitem.rect)
    return player

# -----------------
def update_screen(scene=None):
    screen.blit(master.surf, master.rect)
    for player in players:
        screen.blit(player.figure.image, player.figure.rect)
    screen.blit(sau.figure.image, sau.figure.rect)
    screen.blit(master.marker.image, 
                master.marker.places[master.marker.pos])
    if scene != None:
        board = scene.board
        marker = board.event_marker
        screen.blit(board.surf, board.rect)
        screen.blit(marker.image, marker.places[marker.pos])
        for line in scene.lines:
            screen.blit(line.marker.image, line.marker.places[line.marker.pos])
    for object in current_options:
        screen.blit(object.image, object.rect)
    pygame.display.flip()

# -----------------
# Function to find places in text where there should be a symbol
# Define names of symbols
symbols = ['hiding', 'travelling', 'fighting', 'friendship', # Activity symbols
           'star', 'blacksquare', 'sundial',        # Other symbols
           'eye', 'whitecircle', 'blackcircle',  # Corruption line symbols
           'null']                                 # Null symbol
def replace_symbols(text, fillcol, textcol):
    font = pygame.font.Font(None, 20)
    textsurf = pygame.Surface((600, 25))#screen_size[0], 25))
    textrect = textsurf.fill(fillcol)
    cursor = 0
    substrings = []
    heights = []
    for subtext in text.split(' '):
        for string in subtext.split('['):
            substrings += string.split(']')
    for s, string in enumerate(substrings):
        if string not in symbols:
            output = displayObject(font.render(string+' ', 1, textcol))
        else:
            output = displayObject('symbols/'+string+'.bmp')
        if cursor + output.rect.width >= 600:
            remaining = ' '.join(substrings[s:])
            textrect = textrect.clip(pygame.Rect(0,
                textrect.height-max(heights), cursor, max(heights)))
            return textsurf, textrect, remaining
        heights.append(output.rect.height)
        output.rect.bottomleft = (cursor, textrect.height)
        cursor += output.rect.width
        textsurf.blit(output.image, output.rect)
    textrect = textrect.clip(pygame.Rect(0, textrect.height-max(heights),
                                         cursor, max(heights)))
    print textrect.width
    return textsurf, textrect, None

# -----------------
# Print text to screen.
def print_scr(text_list, wait_time=1000, fillcol=(0,255,63), textcol=(0,0,0)):
    surf = pygame.Surface((600,100))
    rect = surf.fill(fillcol)
    rect.midbottom = screen.get_rect().midbottom
    y = 5
    for text in text_list:
        remaining = 0
        while remaining != None:
            output, text_rect, remaining = replace_symbols(text, fillcol, 
                                                           textcol)
            text_rect.centerx = 300
            text_rect.top = y
            surf.blit(output, text_rect)
            screen.blit(surf, rect)
            pygame.display.update(rect)
            y += 25
            text = remaining
    wait(wait_time)
    return rect

# -----------------
# Print question to screen and return user input
def choose_option(question, options, char, box_col=(0,63,255),
                  fillcol=(0,255,63), textcol=(0,0,0)):
    surfrect = print_scr([question], 0, fillcol, textcol)
    separation = 600/(len(options)+1)
    x = 0
    boxes = {}
    texts = []
    font = pygame.font.Font(None, 20)
    for option in options:
        output, text_rect, null = replace_symbols(option, box_col, textcol)
        texts.append([output, text_rect])
    width = max([text[1].width for text in texts])+10
    if width < 100:
        width = 100
    for t, text in enumerate(texts):
        x += separation
        box = displayObject(pygame.Surface((width,35)))
        box.image.fill(box_col)
        box.rect.centerx = surfrect.left + x
        box.rect.top = surfrect.top + 50
        boxes[box] = t
        text[1].midbottom = box.rect.width/2.0, box.rect.height-10
        box.image.blit(text[0], text[1])
        screen.blit(box.image, box.rect)
        pygame.display.update(box.rect)
    
    selected = choose_button(char, boxes.keys())
    if selected in boxes.keys():
        print_scr([''])
        return boxes[selected]

# -----------------
# Get shields function
# Adds to a players number of shields and checks if Gandalf is callable
def get_shields(char, numshields, scene=None):
    char.shields += numshields
    g = False
    for p in players:
        if p.shields >= 5:
            g = True
            break
    if g == True and gandalf_button not in current_options:
        current_options.append(gandalf_button)
    if g == False and gandalf_button in current_options:
        current_options.remove(gandalf_button)
    print_scr(['You receive '+str(numshields)+' shields',
                'You now have '+str(char.shields)+' shields'], 1000,
                char.displaycolour)
    show_player_stats(char)
    update_screen(scene)

# -----------------
# Draw Hobbit cards
# This function randomly defines the symbol and colour of a hobbit card and appends that card to the player's hand.
random.shuffle(deck)
def draw_hobbit_card(char, numcards, deck=deck):
    cardback = displayObject('/cards/hobbit cards/hobbit_back.jpg')
    cardback.rect.top = master.rect.bottom+60
    x = 0
    separation = screen_size[0]/(numcards+1)
    for n in range(numcards):
        x += separation
        cardback.rect.centerx = x
        screen.blit(cardback.image, cardback.rect)
    update_screen()
    wait(500)
    x = 0
    for n in range(numcards):
        x += separation
        if len(deck) < 1:
            deck = discard_pile
            random.shuffle(deck)
            discard_pile = []
        hobbit = deck[0]
        char.hand.append(hobbit)
        deck.remove(hobbit)
        hobbit.rect.centerx = x
        hobbit.rect.top = master.rect.bottom + 60
        screen.blit(hobbit.image, hobbit.rect)
        update_screen()
        text1 = char.name+' has received:'
        text2 = hobbit.name+','
        for i in hobbit.stats:
            text2 += ' '+i
        print_scr([text1, text2], 100, char.displaycolour)
        if hobbit.colour == 'white' and char == fr:
            hobbit.isfrodojoker = True

# -------------------
# Show cards in a player's hand.
def show_hand(char, hand, choose_card=False, scene=None):
    screen.fill((0,0,0))
    update_screen(scene)
    x = 0
    separation = screen_size[0]/(len(hand)+1)
    for card in hand:
        x += separation
        card.rect.centerx = x
        card.rect.top = master.rect.bottom + 60
        screen.blit(card.image, card.rect)
        pygame.display.update(card.rect)
    if choose_card:
        print_scr(["Choose one of the above cards from "+char.name+"'s hand."])
    else:
        print_scr(["Cards in "+char.name+"'s hand.",'Click to cancel.'])
    looking = True
    while looking:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if choose_card:
                    for card in hand:
                        if card.rect.collidepoint(pos):
                            return card
                else:
                    return

# -------------------
# Distribute Hobbit cards.
# Allows players to distribute four Hobbit cards between them.
def distribute():
    screen.fill((0,0,0))
    print_scr([''])
    cardback = pygame.image.load('./images/cards/hobbit cards/hobbit_back.jpg')
    rect = cardback.get_rect(top=master.rect.bottom+60)
    x = 0
    separation = screen_size[0]/5
    for i in range(4):
        x += separation
        rect.centerx = x
        screen.blit(cardback, rect)
    update_screen()
    wait(500)
    x = 0
    cards = []
    for i in range(4):
        x += separation
        hobbit = deck[0]
        cards.append(hobbit)
        deck.remove(hobbit)
        text1 = 'You have drawn:'
        text2 = hobbit.name+','
        for i in hobbit.stats:
            text2 += ' '+i
        print_scr([text1,text2])
        hobbit.rect.centerx = x
        hobbit.rect.top = master.rect.bottom + 60
        screen.blit(hobbit.image, hobbit.rect)
        update_screen()
        #wait(1500)
    
    while len(cards) > 0:
        pos = pygame.mouse.get_pos()
        print_scr(['Choose a card to distribute'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for card in cards:
                    if card.rect.collidepoint(pos):
                        screen.fill((0,0,0))
                        print_scr(['Select a player or click the card to ' +
                                    'return to card selection.', 
                                   "(Right-click to see player's hand.)"])
                        player = choose_player(players, card)
                        screen.fill((0,0,0))
                        if player != None:
                            player.hand.append(card)
                            cards.remove(card)
                            if card.colour == 'white' and player == fr:
                                card.isfrodojoker = True
                        x3 = 0
                        sep3 = screen_size[0]/(len(cards)+1)
                        for card2 in cards:
                            x3 += sep3
                            card2.rect.centerx = x3
                            card2.rect.top = master.rect.bottom + 60
                            screen.blit(card2.image, card2.rect)
                        update_screen()
    print_scr(['Cards have been distributed'])

# -------------------
# Pass cards.
def pass_cards():
    for p, player in enumerate(players):
        if p == len(players)-1:
            nextplayer = players[0]
        else:
            nextplayer = players[p+1]
        card = show_hand(player, player.hand, True)
        nextplayer.hand.append(card)
        player.hand.remove(card)
        print_scr([nextplayer.name+' has received your card.'])
        wait(1000)

#   ---------------------------
# Discard cards
# This function asks the player which card to discard and removes it from their 
# hand.
def discard(char, card='any', number=1, card2=None, scene=None):
    # Count of the number of cards already discarded
    n_discarded = 0
    # While loop continues until the number of cards discarded reaches the number the player was instructed to discard.
    while n_discarded < number:
        # If the player has discarded one symbol type and now needs to discard another, card becomes equal to card2 so the rest of the function knows what's going on.
        if card2 != None and n_discarded >= 1:
            card = card2

        allowed_cards = []
        if card == 'any':
            allowed_cards = char.hand
        else:
            for c in char.hand:
                if c.symbol == card or c.symbol == 'joker' or c.isfrodojoker:
                    allowed_cards.append(c)
        """
        # Player is eliminated from the game if unable to discard required cards
        if (n_discarded == 0) and (len(allowed_cards) < number):
            c = char_death(char)
            if c == 'next player':
                a = a + 1
                if a > len(players)-1:
                    a = 0
                active_player = players[a]
            return
        """
        disc_card = show_hand(char, allowed_cards, choose_card=True, scene=scene)

        if card == 'any':
            val = 1
        else:
            val = disc_card.value
        if disc_card.name == 'gollum' and card != 'any':
            print_scr(['The Gollum card requires you to roll the dice when '+
                'discarding [star] symbols.'])
            dice(char)
        # The player has come one step closer to discarding the necessary cards.
        char.hand.remove(disc_card)
        n_discarded = n_discarded + val
        text = 'You have discarded '+disc_card.name+','
        for s in disc_card.stats:
            text += ' '+s
        print_scr([text])
        wait(1000)

        if disc_card.name == 'hobbit card':
            discard_pile.append(disc_card)

    return val

# -------------------
# Roll dice
# This function uses random numbers to determine the outcome of a dice roll.
# The variable 'ring' defines the number of spaces a player may move an activity line if they put the Ring on (4 - number of symbols on the dice).
dice_ims = [displayObject(pygame.image.load('./images/dice/one.jpg')),
            displayObject(pygame.image.load('./images/dice/two.jpg')),
            displayObject(pygame.image.load('./images/dice/three.jpg')),
            displayObject(pygame.image.load('./images/dice/cards.jpg')),
            displayObject(pygame.image.load('./images/dice/eye.jpg')),
            displayObject(pygame.image.load('./images/dice/blank.jpg'))]
def dice(char, scene=None, doom=False):
    for im in dice_ims:
        im.rect.centerx = master.rect.centerx
        im.rect.top = master.rect.bottom + 125
    # If a player has the Belt card it may be used to avoid rolling the dice, unless the player is at Mount Doom.
    for p in players:
        if belt in p.hand and doom == False:
            option = choose_option('Would you like to discard the Belt card '+ \
                'to avoid rolling the dice?', ['Yes[null]','No[null]'], scene)
            if option == 0:
                p.hand.remove(belt)
                return
    screen.fill((0,0,0))
    update_screen(scene)
    print_scr(['Rolling the dice...', 'Click to stop.'])
    rolling = True
    while rolling:
        x = random.randint(6)
        screen.blit(dice_ims[x].image, dice_ims[x].rect)
        pygame.display.update(dice_ims[x].rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                rolling = False
        wait(50)
    if x == 0:
        corr = 1
        print_scr(['Move 1 step on corruption line'])
        ring = 3
    elif x == 1:
        corr = 2
        print_scr(['Move 2 steps on corruption line'])
        ring = 2
    elif x == 2:
        corr = 3
        print_scr(['Move 3 steps on corruption line'])
        ring = 1
    elif x == 3:
        print_scr(['Discard two cards'])
        ring = 2
        corr = 0
    elif x == 4:
        corr = -1
        print_scr(['Sauron moves'])
        ring = 3
    elif x == 5:
        print_scr(['Nothing happens'])
        wait(1000)
        return 4
    wait(1000)
    
    # If the player has the Mithril card it may be used to ignore the dice roll.
    for p in players:
        if mithril in p.hand:
            option = choose_option('Would you like to discard the Mithril '+ \
                'card to ignore the effects of this dice-roll?',
                ['Yes[null]','No[null]'], scene, box_col=p.displaycolour)
            if option == 0:
                p.hand.remove(mithril)
                return ring
    
    # The player moves on the corruption line, or Sauron moves, or the player 
    # discards two cards, as determined above.
    if corr > 0:
        if char == sa:
            corr = 1
        char.increase_corruption(corr)
    elif corr < 0:
        sau.move_sauron()
    
    elif corr == 0:
        # Discard a card
        discard(char)
        # Everyone but Sam discards a second card.
        if char != sa:
            discard(char)
        pass
    
    return ring

# -----------------
# The Ring.
# This function moves an activity line chosen by the player the appropriate number of spaces.
def ring(r, scenario):
    print_scr(['Choose an activity line to move'])
    x = 0
    sep = screen_size[0]/(len(scenario.show_tiles)+1)
    for tile in scenario.show_tiles:
        x += sep
        tile.rect.centerx = x
        tile.rect.top = master.rect.bottom + 60
        screen.blit(tile.image, tile.rect)
        pygame.display.update(tile.rect)
    chosen_line, right_click = standard_loop(scenario.show_tiles)
    line = chosen_line.move

    line.pos = line.pos + r
    for space in range(r):
        skip = line.readfile.readline()
        if skip == 'card\n':
            skip = line.readfile.readline()
        line.marker.move()
        update_screen(scenario)
    print_scr(['The '+line.name+' line is now on space '+str(line.pos)])

# --------------------
# Activity lines.
def moveline(char, line, scene, spaces=1):#, shields=shlds):
    available = scene.features
    getfile = line.readfile
    shields_gained = 0
    for i in range(spaces):
        line.pos = line.pos + 1
        line.marker.move(scene)
        if line.pos == line.end:
            line.scene.finished_lines.append(line.name)
            for tile in scene.show_tiles:
                if tile.move == line:
                    scene.show_tiles.remove(tile)
        getstuff = getfile.readline()
        if getstuff == 'shield\n':
            shields_gained += 1
            #char.shields = char.shields + 1
        elif getstuff == 'ring\n':
            char.tokens[0] = char.tokens[0] + 1
            print_scr(['You receive one ring token', 
                       'You now have '+str(char.tokens[0])+' ring tokens'],
                       fillcol=char.displaycolour)
        elif getstuff == 'heart\n':
            char.tokens[1] = char.tokens[1] + 1
            print_scr(['You receive one heart token', 
                       'You now have '+str(char.tokens[1])+' heart tokens'],
                       fillcol=char.displaycolour)
        elif getstuff == 'sun\n':
            char.tokens[2] = char.tokens[2] + 1
            print_scr(['You receive one sun token', 
                       'You now have '+str(char.tokens[2])+' sun tokens'],
                       fillcol=char.displaycolour)
        elif getstuff == 'dice\n':
            print_scr(['You must roll the dice'], fillcol=char.displaycolour)
            dice(char, scene)
        elif getstuff == 'card\n':
            cardnum = getfile.readline()
            c = int(cardnum)
            card = linecards[c]
            if available == True:
                card.rect.center = scene.board.rect.center
                screen.blit(card.image, card.rect)
                pygame.display.update(card.rect)
                print_scr(['You receive the '+card.name+' card'],
                          fillcol=char.displaycolour)
                char.hand.append(card)
            else:
                print_scr(['You do not receive the '+card.name+ \
                    ' card because it has been discarded.'],
                    fillcol=char.displaycolour)
        elif getstuff == 'step back':
            print_scr(['You take one step back on the corruption line'],
                      fillcol=char.displaycolour)
            char.increase_corruption(-1)
        elif getstuff == 'big shield\n':
            print_scr(['You receive a big shield...'],
                      fillcol=char.displaycolour)
            s = shields.readline()
            print_scr(["It's a"+s+'!'], fillcol=char.displaycolour)
            char.shields = char.shields + int(s)
    if shields_gained > 0:
        get_shields(char, shields_gained, scene)
    print_scr(['The '+line.name+' line is now on space '+str(line.pos)])

# -----------------
# Defines and shuffles event tiles
def define_tiles(scene):
    fight = event_tile('fighting', scene.fighting, 
        'Move the [fighting] line one space', 'activity', 'fighting.jpg')
    hide = event_tile('hiding', scene.hiding, 
        'Move the [hiding] line one space', 'activity', 'hiding.jpg')
    trav = event_tile('travelling', scene.travelling, 
        'Move the [travelling] line one space.', 'activity', 'travelling.jpg')
    friend = event_tile('friendship', scene.friendship,
        'Move the [friendship] line one space', 'activity', 'friendship.jpg')
    rbm1 = event_tile('Ring-bearer move one', 'bearer',
        'Ring-bearer must [blackcircle]', 'other', 'ring.jpg')
    two_or_one = event_tile('Move one player or Sauron', 'player',
        'One player must volunteer to [blackcircle][blackcircle] or [eye]',
        'other', 'eye_circles.jpg')
    sundial = event_tile('sundial', 'event', 'The next event occurs.', 'other',
        'sundial.jpg')
    three_cards = event_tile('Three cards or sundial', 'none',
        'The group must discard three cards or the next event occurs',
        'disc_or_event', 'sundial_cards.jpg')
    three_items = event_tile('Three items or sundial', 'none', 'The group '+ \
        'must discard a life token, a card & a shield or the next event occurs',
        'disc_or_event', 'sundial_items.jpg')

    tiles = []
    for i in range(3):
        tiles.append(fight)
        tiles.append(hide)
        tiles.append(trav)
        tiles.append(friend)
    for i in range(2):
        tiles.append(rbm1)
    for i in range(6):
        tiles.append(sundial)
    tiles.append(two_or_one)
    tiles.append(three_cards)
    tiles.append(three_items)

    random.shuffle(tiles)
    return tiles

# Define the reveal event tile button
tile_button = displayObject('tiles/tile_back.jpg')
tile_button.rect.midtop = (100, 250)

# -----------------
# Events.
# Template for all events. Does the same thing each time to save me a load of
# coding, but calls to separate functions to carry out individual bits of events
def scene_event(char, scenario, event_number, ring_bearer):
    this_event = scenario.events[event_number]
    event_type = this_event[4]
    print_scr(this_event[3])
    wait(1000)
    options = this_event[2]
    
    if event_type == 'each player':
        rangelist = players
    else:
        rangelist = [char]

    for char in rangelist:
        while 1:
            action = choose_option(char.name+', what would you like to do?',
                                   options, scenario, box_col=char.displaycolour)
            if action == len(options)-1:
                while 2:
                    other_options = ['Play a yellow card', 'Put the Ring on']
                    """
                    g = 'n'
                    for i in players:
                        if i.shields >= 5:
                            g = 'y'
                            break
                    if g == 'y':
                        other_options.append('Call Gandalf')
                    """
                    action2 = choose_option('What would you like to do?',
                                            other_options, scenario,
                                            box_col=char.displaycolour)
                if action2 == 0:
                    yellow()
                if action2 == 1:
                    if ring_bearer.ring != True:
                        print_scr(['The Ring-bearer must [blacksquare]'])
                        r = dice(ring_bearer, scenario)
                        ring(r, scenario)
                        ring_bearer.ring = True
                        if scenario.main.pos >= scenario.main.end:
                            return 'end'
                    else:
                        print_scr(['The Ring-bearer is already wearing the Ring',
                         'It will be removed at the end of the current scenario'])
                """
                if action2 == 2:
                    sh_pl = choose_player()
                    while 2:
                        print "Which of Gandalf's abilities would you like to use? [Pick a number]"
                        for j, ability in enumerate(gandalfs):
                            print j, ':', ability.name, '(', ability.description, ')'
                        try:
                            g = input()
                        except:
                            print 'Please type in a number between 0 and', len(gandalfs)-1, '.'
                            continue
                        if g > len(gandalfs)-1:
                            print "That's not an available option. Pick a number between 0 and", len(options)-1, '.'
                            continue
                        break
                    sh_pl.shields = sh_pl.shields - 5
                    gand = gandalfs[g]
                    if gand == magic:
                        print 'The current event has been ignored.'
                        gandalfs.remove(magic)
                        return
                    elif gand == guidance:
                        gand(char, scenario)
                    else:
                        gand()
                    
                    gandalfs.remove(gand)
                """
            else:
                event = this_event[action](char, scenario)
                if event == 'next':
                    return event
                if event == 'loop':
                    continue
                if event == 'features':
                    return event
                break

# -----------------
# Call Gandalf function
# Doesn't actually do anything yet
def call_gandalf():
        print_scr(['Unfortunately, Gandalf has wandered off', 
         'Try again later'])

# -----------------
# Start of go stuff. Because it may as well be here.
def start_go(scenario, active_player):
    #start_options = scenario.current_options + [tile_button]
    screen.fill((0,0,0))
    update_screen(scenario)
    screen.blit(tile_button.image, tile_button.rect)
    pygame.display.update(tile_button.rect)
    print_scr([active_player.name+', it is your turn to reveal a tile'])
    #for option in start_options:
    #    screen.blit(option.image, option.rect)
    #    pygame.display.update(option.rect)
    #selected, right_click = standard_loop(start_options)
    #if selected == tile_button:
    #    return
    selected = None
    while selected != tile_button:
        selected = choose_button(active_player, [tile_button])
    """
    elif selected == ring_button:
        if ring_bearer.ring != True:
            print_scr(['The Ring-bearer must [blacksquare]'])
            r = dice(ring_bearer, scenario)
            ring(r, scenario)
            ring_bearer.ring = True
            start_options.remove(ring_button)
            scenario.extra_objects.remove(ring_button)
            if scenario.main.pos >= scenario.main.end:
                return 'end'
        else:
            print_scr(['The Ring-bearer is already wearing the Ring',
                       'It will be removed at the end of the current scenario'])
        return 'more tiles'
    elif selected == gandalf_button:
        call_gandalf()
        return 'more tiles'
    """
    """
    elif action == 2:
        ph = False
        for p in players:
            if phial in p.hand:
                ph = choose_option('Would the active player like to use the '+ \
                    'phial card and stop drawing tiles?',
                    ['Yes[null]', 'No[null]'],
                    box_col=active_player.displaycolour)
        if ph == 0:
            return 'stop tiles'
        yellow()
    elif action == 3:
        sh_pl = choose_player()
        while 2:
            print "Which of Gandalf's abilities would you like to use? [Pick a number]"
            for j, ability in enumerate(gandalfs):
                print j, ':', ability.name, '(', ability.description, ')'
            try:
                g = input()
            except:
                print 'Please type in a number between 0 and', len(gandalfs)-1, '.'
                continue
            if g > len(gandalfs)-1:
                print "That's not an available option. Pick a number between 0 and", len(options)-1, '.'
                continue
            break

        gand = gandalfs[g]
        if gand == magic:
            print 'That is not an available option at the moment as you are not currently carrying out an event.'
        elif gand == guidance:
            gand(active_player, scenario)
        elif gand == foresight:
            gand(scenario.tiles)
        else:
            gand()

        if gand != magic:
            sh_pl.shields = sh_pl.shields - 5
            gandalfs.remove(gand)
    """
# -----------------
# End of go stuff. Because it may as well be here.
def end_go(scenario, active_player):
    endgo_buttons = [master, scenario.board, hobbit_button]
    print_scr(['Click the master board to [whitecircle]',
               'Click the scenario board to play cards',
               'Click the Hobbit deck to draw 2 cards'])
    selected = choose_button(active_player, endgo_buttons)
    if selected == scenario.board:
        old_colour = None
        for played in range(2):
            allowed_cards = []
            for c in active_player.hand:
                if (c.symbol != scenario.noline or c.isfrodojoker) \
                and c.colour != 'yellow' and (c.colour != old_colour or active_player == pi) \
                and c.symbol not in scenario.finished_lines:
                    allowed_cards.append(c)
            if len(allowed_cards) == 0:
                print_scr(['Sorry, there are no cards you can play at this time',
                           'Try again later'])
                continue
            old_colour = play_cards(active_player, scenario, allowed_cards, 
                                    old_colour)
            if played < 1:
                option = choose_option('Would you like to play another card?',
                                       ['[null]Yes', '[null]No'], scenario,
                                       box_col=active_player.displaycolour)
                if option != 0:
                    return
    elif selected == hobbit_button:
        draw_hobbit_card(active_player, 2)
    elif selected == master:
        active_player.increase_corruption(-1)

# -----------------
# Playing cards for the end of one's go.
def play_cards(char, scenario, allowed, old_colour):
    play_card = show_hand(char, allowed, True, scenario)
    if play_card.symbol == 'joker' or play_card.isfrodojoker:
        screen.fill((0,0,0))
        update_screen(scenario)
        print_scr(['What would you like to use that joker as?'])
        x = 0
        sep = screen_size[0]/(len(scenario.show_tiles)+1)
        for tile in scenario.show_tiles:
            x += sep
            tile.rect.centerx = x
            tile.rect.top = master.rect.bottom + 60
            screen.blit(tile.image, tile.rect)
            pygame.display.update(tile.rect)
        chosen_line, right_click = standard_loop(scenario.show_tiles)
        move = chosen_line.move
    else:
        if play_card.symbol == 'fighting':
            move = scenario.fighting
        elif play_card.symbol == 'hiding':
            move = scenario.hiding
        elif play_card.symbol == 'travelling':
            move = scenario.travelling
        elif play_card.symbol == 'friendship':
            move = scenario.friendship

    spaces = play_card.value
    moveline(char, move, scenario, spaces)
    old_colour = play_card.colour
    char.hand.remove(play_card)
    return play_card.colour

# -----------------
# Initiate screen and so on
pygame.init()
icon = pygame.image.load("./images/onering.png")
pygame.display.set_icon(icon)
screen_size = (1300, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("The Lord of the Rings")
wait = pygame.time.wait

# Define master board
master = masterBoard()

# Define the ring
ring_button = displayObject('thering.bmp', 100, 100)

# Define the Call Gandalf button
gandalf_button = displayObject('cards/gandalf/button.jpg', 250, 100)
#gandalf_button.rect.center = (250,100)

# Define the draw Hobbit cards button
hobbit_button = displayObject('cards/hobbit cards/hobbit_back.jpg')
hobbit_button.rect.midtop = 250, tile_button.rect.top

# Put yellow card buttons in the right place
yellows = [athelas, miruvor, mithril, staff,
           belt, elessar, lembas, phial]
yellow_icons = [card.icon for card in yellows]
y = 50
x = master.rect.right + 50
for card in yellows:
    card.icon.rect.center = x, y
    x += 80
    if x > master.rect.right + 300:
        x = master.rect.right + 50
        y += 80

current_options = [ring_button]

# Create life token and shield icons
ring_icon = displayObject('/life tokens/ring.bmp')
heart_icon = displayObject('/life tokens/heart.bmp')
sun_icon = displayObject('/life tokens/sun.bmp')
token_icons = [ring_icon, heart_icon, sun_icon]
x = 130
for token in token_icons:
    token.rect.midbottom = x, 215
    x += 80
shield_icon = displayObject('/shield.bmp', 50, 165)

# Define show character's hand icon
hand_icon = displayObject('cards/hobbit cards/hobbit_back_small.jpg', 200, 50)

icons = token_icons + [shield_icon, hand_icon]

# Creates each player and Sauron
fr = Hobbit('Frodo', (255,255,0,))
sa = Hobbit('Sam', (255,0,0))
pi = Hobbit('Pippin', (0,255,0))
me = Hobbit('Merry', (0,63,255))
fa = Hobbit('Fatty', (255,127,0))
sau = dark_lord()

# Define the text describing each character's special attribute.
fr.powerblurb = 'Use any white Hobbit cards as [star] cards'
sa.powerblurb = 'After each die roll suffer no more than one damage'
pi.powerblurb = 'On your turn play any 2 cards'
me.powerblurb = 'After each scenario you only need 2 different Life tokens'
fa.powerblurb = 'After each scenario draw 2 Hobbit cards'

# List of all players.
players = [fr, sa, pi, me, fa]
player_icons = [player.icon for player in players]
player_figs = [player.figure for player in players]

# Sets initial Ring-bearer.
ring_bearer = fr
