from lotr_mod import *
from scenario_template import *
from moria_ import *

# Select number of players
x = 0
sep = screen_size[0]/6
for player in players:
    x += sep
    card = player.char_card
    card.rect.top = master.rect.bottom + 60
    card.rect.centerx = x
num = choose_num_players()

for i in range(4, num-1, -1):
    players.remove(players[i])
x = master.rect.right# + 10
sep = (screen_size[0]-master.rect.right)/(len(players)+1)
for player in players:
    x += sep
    player.icon.rect.midbottom = x, screen_size[1]#master.rect.bottom + 300
    current_options.append(player.icon)


# Puts hobbits in the correct place on the corruption line
y = master.rect.top + 135
for p in players:
    p.figure.rect.top = y
    y += 10
update_screen()

# Defines the lack of scenario
scene = None

#--------------------------------------------------

wait(500)
print_scr(['-------------------',
          '|      Bag End      |',
           '-------------------'])
wait(1000)

# Everyone receives six Hobbit cards.
print_scr(['--- Gandalf ---', 
           'EACH PLAYER: Receive 6 Hobbit cards.'], 2000)
for player in players:
    draw_hobbit_card(player, 6)
   # wait(3000)
    screen.fill((0,0,0))
    update_screen()
    print_scr([''])
    #wait(2000)

    #===============
"""
# Player may, if they choose, roll the dice (function from lotr_mod) and 
# distribute four Hobbit cards.
print_scr(['--- Preparations ---', 
           'Ring-bearer may [blacksquare] and reveal 4 hobbit cards face up '+
           'for distribution.'])
wait(2000)
option = choose_option('Would the Ring-bearer like to roll the dice?', 
                       ['Yes, [blacksquare]', "No, I'll play it safe[null]"],
                       box_col=ring_bearer.displaycolour)
if option == 0:
    dice(ring_bearer)
    distribute()

    #===============

# Player must discard two hiding symbols.
print_scr(['--- Nazgul appears ---', 
           'One player discard 2 [hiding] otherwise [eye]'])
wait(2000)

players_with_hidings = []
# Counts discardable cards in each player's hand.
for plr in players:
    hidings = 0
    for card in plr.hand:
        if card.symbol == 'hiding' or card.symbol == 'joker' or \
         card.isfrodojoker:
            hidings = hidings + 1
    if hidings >= 2:
        players_with_hidings.append(plr)

print_scr(['Choose a player to discard 2 [hiding] '+
            'or click the eye to move Sauron.',
            "(Right-click to see player's hand)"])
player = choose_player(players_with_hidings, dice_ims[4])
if player == None:
    sau.move_sauron()
else:
    print_scr([player.name+' will discard 2 [hiding]'])
    discard(player, 'hiding', 2)

screen.fill((0,0,0))
update_screen()
print_scr([''])
wait(1000)
"""
#--------------------------------------------------

master.move_marker()
print_scr(['---------------------',
          '|      Rivendell      |',
           '---------------------'])
wait(1000)

print_scr(['--- Elrond ---',
           'Receive feature cards.'])
wait(1000)

rivendell = shuffle_rivendell()
k = 0
riv = dict(zip(players, [[],[],[],[],[]]))
while k < 12:
    for player in players:
        if len(players) < 3 and k == 8:
            k = 12
        if k == 12:
            break
        riv[player].append(rivendell[k])
        k = k+1

cardback = displayObject('/cards/feature cards/card_back.jpg')
cardback.rect.top = master.rect.bottom + 60
for player in players:
    numcards = len(riv[player])
    player.hand += riv[player]
    x = 0
    sep = screen_size[0]/(numcards+1)
    screen.fill((0,0,0))
    for n in range(numcards):
        x += sep
        cardback.rect.centerx = x
        screen.blit(cardback.image, cardback.rect)
    update_screen()
    print_scr([''])
    x = 0
    for fcard in riv[player]:
        x += sep
        fcard.rect.centerx = x
        fcard.rect.top = master.rect.bottom + 60
        screen.blit(fcard.image, fcard.rect)
        if fcard.colour == 'yellow':
            screen.blit(fcard.icon.image, fcard.icon.rect)
            current_options.append(fcard.icon)
        update_screen()
        text1 = player.name+' has received:'
        text2 = fcard.name+','
        for i in fcard.stats:
            text2 += ' '+i
        print_scr([text1, text2], 200, player.displaycolour)
screen.fill((0,0,0))

    #===============
"""
# Each player must pass a card to the next player.
print_scr(['--- Council ---',
           'EACH PLAYER: pass one card face down to the left'])
wait(2000)

pass_cards()

    #===============

# All players must discard a friendship symbol.
screen.fill((0,0,0))
print_scr(['--- Fellowship ---',
           'EACH PLAYER: Discard [friendship] otherwise [blacksquare].'])
wait(2000)

for p in players:
    screen.fill((0,0,0))
    allowed_cards = []
    for c in p.hand:
        if c.symbol == 'friendship' or c.symbol == 'joker' or c.isfrodojoker:
            allowed_cards.append(c)
    option = choose_option(p.name+', would you like to discard a [friendship]?',
                           ['Yes, discard [friendship]', 'No, [blacksquare]'],
                            box_col=p.displaycolour)
    if option == 0:
        if len(allowed_cards) > 0:
            discard(p, 'friendship')
        else:
            print_scr(['You do not have enough cards of that type'])
            wait(1000)
            dice(p)
    else:
        dice(p)
"""
#   -------------------------------------------------------

master.move_marker()
print_scr(['-----------------',
          '|      Moria      |',
           '-----------------'], 2000)

scene = moria
update_screen(scene)
ring_bearer = play_scenario(scene, ring_bearer)

#   -------------------------------------------------------

master.move_marker()
print_scr(['----------------------',
          '|      Lothlorien      |',
           '----------------------'], 2000)

# As in Rivendell, cards are shuffled and dealt.
print_scr(['--- Galadriel ---',
           'Receive feature cards.'])

lothlorien = shuffle_loth()
k = 0
loth = dict(zip(players, [[],[],[],[],[]]))
while k < 12:
    for player in players:
        if len(players) < 3 and k == 8:
            k = 12
        if k == 12:
            break
        loth[player].append(lothlorien[k])
        k = k+1

cardback = displayObject('/cards/feature cards/card_back.jpg')
cardback.rect.top = master.rect.bottom + 60
for player in players:
    numcards = len(loth[player])
    player.hand += loth[player]
    x = 0
    sep = screen_size[0]/(numcards+1)
    screen.fill((0,0,0))
    for n in range(numcards):
        x += sep
        cardback.rect.centerx = x
        screen.blit(cardback.image, cardback.rect)
    update_screen()
    print_scr([''])
    wait(500)
    x = 0
    for fcard in loth[player]:
        x += sep
        fcard.rect.centerx = x
        fcard.rect.top = master.rect.bottom + 60
        screen.blit(fcard.image, fcard.rect)
        if fcard.colour == 'yellow':
            screen.blit(fcard.icon.image, fcard.icon.rect)
            current_options.append(fcard.icon)
        update_screen()
        text1 = player.name+' has received:'
        text2 = fcard.name+','
        for i in fcard.stats:
            text2 += ' '+i
        print_scr([text1, text2], 200, player.displaycolour)
        #wait(1500)
screen.fill((0,0,0))
update_screen()
print_scr([''])

    #===============
"""
print_scr(['--- Recovery ---',
          'EACH PLAYER: May discard 2 shields to either draw 2 Hobbit cards '+
          'or [whitecircle]'])

for player in players:
    if player.shields >= 2:
        option = choose_option(player.name+', would you like to discard 2 '+
                                'shields?',
                                ['Yes, discard shields[null]', 
                                "No, I'll hold on to them[null]"],
                                box_col=player.displaycolour)
        if option == 0:
            player.shields = player.shields - 2
            option = choose_option('What would you like to do?',
                                   ['Draw two Hobbit cards[null]',
                                   '[whitecircle]'],
                                   box_col=player.displaycolour)
            if option == 0:
                draw_hobbit_card(player, 2)
            elif option == 1:
                player.increase_corruption(-1)
    else:
        print_scr([player.name+', you do not have enough shields to discard.'])

    #===============

# Each player discards a joker.
screen.fill((0,0,0))
print_scr(['--- Test of Galadriel ---',
           'EACH PLAYER: Discard [star] otherwise [blackcircle]'])
wait(2000)

for p in players:
    screen.fill((0,0,0))
    allowed_cards = []
    for c in p.hand:
        if c.symbol == 'joker' or c.isfrodojoker:
            allowed_cards.append(c)
    option = choose_option(p.name+', would you like to discard a [star]?',
                           ['Yes, discard [star]', 'No, [blacksquare]'],
                           box_col=p.displaycolour)
    if option == 0:
        if len(allowed_cards) > 0:
            discard(p, 'joker')
        else:
            print_scr(['You do not have enough cards of that type'])
            wait(1000)
            dice(p)
    else:
        dice(p)

#   -------------------------------------------------------
"""
screen.fill((0,0,0))
update_screen(scene)
print_scr([''])
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
