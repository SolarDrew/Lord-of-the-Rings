from lotr_mod import *

# Speak friend and enter.
def otherwise1(char, scenario):
    sau.move_sauron()
    
def main_option1(char, scenario):
    """
    gand = False
    guide_available = False
    for i in players:
        if i.shields > 4:
            gand = True
    if guidance in gandalfs and gand == True:
        guide_available = True
    
    if guide_available == True:
        options = ['Discard cards', 'Call Gandalf to discard two star symbols']
        while 2:
            print_scr([char.name, ', what would you like to do? [Pick a number]'
            for j, opt in enumerate(options):
                print_scr([j, ':', opt
            try:
                action = input()
            except:
                print_scr(['Please type in a number between 0 and', len(options)-1, '.'
                continue
            if action > len(options)-1:
                print_scr(["That's not an available option. Pick a number between 0 and", len(options)-1, '.'
                continue
            break
        if action == 1:
            sh_pl = choose_player()
            sh_pl.shields = sh_pl.shields - 5
            gandalfs.remove(guidance)
            print_scr(['Gandalf has discarded two star symbols for you. Slacker.'
            return
    """
    players_with_friendships = []
    players_with_jokers = []
    for p in players:
        friendships = False
        for c in p.hand:
            if c.symbol == 'friendship' or c.symbol == 'joker' or \
             c.isfrodojoker:
                friendships = True
                break
        if friendships:
            players_with_friendships.append(p)
    for p in players:
        jokers = False
        for c in p.hand:
            if c.symbol == 'joker' or c.isfrodojoker:
                jokers = True
                break
        if jokers:
            players_with_jokers.append(p)

    if len(players_with_friendships) < 1 or len(players_with_jokers) < 1:
        print_scr(['The players do not have the required cards'])
        otherwise1(char, scenario)
        return

    print_scr(['Choose a player to discard a [friendship]',
     "(Right-click to see players' cards)"])
    player = choose_player(players_with_friendships, None, scenario)
    discard(player, 'friendship', 1, None, scenario)
    
    print_scr(['Choose a player to discard a [star]',
     "(Right-click to see players' cards)"])
    player = choose_player(players_with_jokers)
    discard(player, 'joker', 1, None, scenario)
    return

options1 = ['Discard cards[null]', '[eye]']

####

# Watcher in the water
def otherwise2(char, scenario):
    dice(char, scenario)

def main_option2(char, scenario):
    hidey = False
    for card in char.hand:
        if card.symbol == 'hiding' or card.isfrodojoker:
            hidey = True
    if hidey == True:
        discard(char, 'hiding', 1, None, scenario)
    else:
        print_scr(['You do not have a [hiding] symbol to discard', 
                   'You must [blacksquare] instead'])
        otherwise2(char, scenario)

options2 = ['Discard [hiding]', '[blacksquare]']

####

# Stone in the well
def otherwise3(char, scenario):
    sau.move_sauron()
    return 'next'

def main_option3(char, scenario):
    """
    gand = False
    guide_available = False
    for i in players:
        if i.shields > 4:
            gand = True
    if guidance in gandalfs and gand == True:
        guide_available = True
    """
    hobbit = deck[0]
    deck.remove(hobbit)
    discard_pile.append(hobbit)
    discard_sym = hobbit.symbol
    hobbit.rect.centerx = master.rect.centerx
    hobbit.rect.top = master.rect.bottom + 75
    screen.blit(hobbit.image, hobbit.rect)
    pygame.display.update(hobbit.rect)
    print_scr(['You have revealed a '+discard_sym])
    """
    if guide_available == True:
        options = ['Discard cards', 'Call Gandalf to discard two star symbols']
        while 2:
            print_scr([char.name, ', what would you like to do? [Pick a number]'
            for j, opt in enumerate(options):
                print_scr([j, ':', opt
            try:
                action = input()
            except:
                print_scr(['Please type in a number between 0 and', len(options)-1, '.'
                continue
            if action > len(options)-1:
                print_scr(["That's not an available option. Pick a number between 0 and", len(options)-1, '.'
                continue
            break
        if action == 1:
            sh_pl = choose_player()
            sh_pl.shields = sh_pl.shields - 5
            gandalfs.remove(guidance)
            print_scr(['Gandalf has discarded two star symbols for you. Slacker.'
            return
    """
    symbolz = 0
    for card in char.hand:
        if card.symbol == discard_sym or card.symbol == 'joker' or \
         card.isfrodojoker:
            symbolz += card.value
    if symbolz > 1:
        discard(char, discard_sym, 2)
        char.hand.append(pipe)
        pipe.rect.center = scenario.board.rect.center
        screen.blit(pipe.image, pipe.rect)
        pygame.display.update(pipe.rect)
        print_scr(['You have received the Pipe card'])
    else:
        print_scr(['You do not have two '+discard_sym+' symbols to discard',
                  '[eye] and the next event will occur'])
        sau.move_sauron()
        return 'next'

options3 = ['Reveal a card[null]', '[eye] and [sundial]']

####

# Trapped?
def otherwise4(char, scenario):
    pass

def main_option4(char, scenario, bear=ring_bearer):
    hide_left = 7 - scenario.hiding.pos
    trav_left = 7 - scenario.travelling.pos
    if hide_left > 0 or trav_left > 0:
        print_scr(['The [hiding] line has {} spaces left'.format(hide_left),
                   'The [travelling] line has {} spaces left'.format(trav_left),
                   '[eye][eye] and Ring-bearer [blacksquare]'])
        sau.move_sauron(2)
        dice(bear, scenario)
    else:
        print_scr(['The [travelling] and [hiding] lines are complete',
                   'Nothing happens'])

options4 = ["Ok"]

####

# Orcs attack
def otherwise5(char, scenario):
    sau.move_sauron(2)

def main_option5(char, scenario):
    """
    gand = False
    guide_available = False
    for i in players:
        if i.shields > 4:
            gand = True
    if guidance in gandalfs and gand == True:
        guide_available = True
    """
    n_to_discard = 5
    available = 0
    for player in players:
        for card in player.hand:
            if card.symbol == 'fighting' or card.symbol == 'joker' or \
             card.isfrodojoker:
                available = available + card.value
    if (available < n_to_discard and guide_available == False) or (guide_available == True and available < (n_to_discard-2)):
        print_scr(['You do not have enough fightings to discard'])
        otherwise5(char, scenario)
        return
    
    while n_to_discard > 0:
        """
        gand = False
        guide_available = False
        for i in players:
            if i.shields > 4:
                gand = True
        if guidance in gandalfs and gand == True:
            guide_available = True

        if guide_available == True:
            options = ['Discard fighting symbols', 'Call Gandalf to discard two star symbols']
            while 2:
                print_scr([char.name, ', what would you like to do? [Pick a number]'
                for j, opt in enumerate(options):
                    print_scr([j, ':', opt
                try:
                    action = input()
                except:
                    print_scr(['Please type in a number between 0 and', len(options)-1, '.'
                    continue
                if action > len(options)-1:
                    print_scr(["That's not an available option. Pick a number between 0 and", len(options)-1, '.'
                    continue
                break
            if action == 1:
                sh_pl = choose_player()
                sh_pl.shields = sh_pl.shields - 5
                n_to_discard = n_to_discard - 2
                gandalfs.remove(guidance)
                print_scr(['Gandalf has discarded two star symbols for you. Slacker.'
                continue
        """
        players_with_fightings = []
        for p in players:
            fights = False
            for c in p.hand:
                if c.symbol == 'fighting' or c.symbol == 'joker' or \
                 c.isfrodojoker:
                    fights = True
                    break
            if fights:
                players_with_fightings.append(p)
            
        player = choose_player(players_with_fightings)
        n_discarded = discard(players_with_fightings[playernum], 'fighting')
        n_to_discard -= n_discarded

options5 = ['Discard fightings[null]', 'Move Sauron[null]']

####

# Fly, you fools!
def otherwise6(char, scenario):
    for p in players:
        dice(p, scenario)

def main_option6(char, scenario):
    player = choose_player(players)
    player.increase_corruption(3)

options6 = ['Move one player[null]', 'All [blacksquare]']

# -----------------
# Define list of events.
moria1 = [main_option1, otherwise1, options1, ['--- Speak friend and enter ---',
            'Group discard [friendship] and [star] otherwise [eye]'], '']
moria2 = [main_option2, otherwise2, options2, ['--- Watcher in the water ---',
            'EACH PLAYER: Discard [hiding] otherwise [blacksquare]'],
            'each player']
moria3 = [main_option3, otherwise3, options3, ['--- Stone in the well ---',
            'Reveal one hobbit card from the deck and Active player discard '+ \
             '2 matching card symbols to receive Pipe card, otherwise [eye] '+ \
             'and next event'], '']
moria4 = [main_option4, otherwise4, options4, ['--- Trapped? ---', 
            'Travelling and Hiding must be complete, otherwise [eye][eye] '+ \
             'and Ring-bearer [blacksquare]'], '']
moria5 = [main_option5, otherwise5, options5, ['--- Orcs attack ---',
            'Group discard 5 [fighting] otherwise [eye][eye]'], '']
moria6 = [main_option6, otherwise6, options6, ['--- Fly you fools! ---',
            'One player [blackcircle][blackcircle][blackcircle] otherwise '+\
             'each player [blacksquare]'], '']
moria_events = [moria1, moria2, moria3, moria4, moria5, moria6]

# -----------------
# Initiate scenario.
moria = scenario('Moria', moria_events)
