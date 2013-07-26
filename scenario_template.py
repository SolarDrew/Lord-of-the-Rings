from lotr_mod import *

def play_scenario(scenario, ring_bearer):
    for line in scenario.lines:
        line.scene = scenario

    mainline = scenario.main
    mainline.pos = scenario.main_start

    if ring_bearer == fr:
        a = 0
    elif ring_bearer == sa:
        a = 1
    elif ring_bearer == pi:
        a = 2
    elif ring_bearer == me:
        a = 3
    elif ring_bearer == fa:
        a = 4

    active_player = players[a]
    players[a].active = True

    scenario.tiles = define_tiles(scenario)
    tiles = scenario.tiles

    while 'tiles':
        go = start_go(scenario, active_player)

        if go == 'end':
            print_scr(['You have finished.'])
            break
        elif go == 'stop tiles':
            end_go(scenario, active_player)
            a = a + 1
            if a > len(players)-1:
                a = 0
            active_player = players[a]
            continue
        elif go == 'more tiles':
            continue
        
        ti = tiles[0]
        #scenario.extra_objects.append(ti)
        update_screen(scenario)
        screen.blit(ti.image, ti.rect)
        pygame.display.update(ti.rect)
        print_scr([active_player.name+", you have drawn a '"+ti.name+"' tile."])
        print_scr([ti.description])
        
        if ti.tile_type == 'disc_or_event':
            # If one player has the Staff card it may be used to ignore the tile.
            for p in players:
                if staff in p.hand:
                    option = choose_option('Would you like to discard the '+ \
                        'Staff card to ignore the effects of this event tile?', 
                        ['Yes, discard the Staff[null]',
                        "No, I'll save it for later[null]"],
                        scenario, box_col=p.displaycolour)
                    if option == 0:
                        p.hand.remove(staff)
                        ti.name = 'ignored'
                        print_scr(['You have ignored the event tile and may '+ \
                            'move on to the next one.'])
            if ti.name == 'Three cards or sundial':
                total_cards = 0
                for p in players:
                    total_cards += len(p.hand)
                print_scr(['The group has a total of '+str(total_cards)+ \
                    ' cards'])
                choice = choose_option('What would you like to do?',
                                       ['Discard three cards[null]', 
                                       'Progress to the next event[null]'],
                                       scenario)
                if total_cards < 3:
                    choice = 1
                if choice == 0:
                    for card in range(3):
                        player = choose_player(players, None, scenario)
                        discard(player, 'any', 1, None, scenario)
                elif choice == 1:
                    ti.move = 'event'
            elif ti.name == 'Three items or sundial':
                total_cards = 0
                players_with_cards = []
                total_tokens = 0
                players_with_tokens = []
                total_shields = 0
                players_with_shields = []
                for p in players:
                    if len(p.hand) > 0:
                        players_with_cards.append(p)
                    total_cards = total_cards + len(p.hand)
                for p in players:
                    if sum(p.tokens) > 0:
                        players_with_tokens.append(p)
                    total_tokens = total_tokens + sum(p.tokens)
                for p in players:
                    if p.shields > 0:
                        players_with_shields.append(p)
                    total_shields = total_shields + p.shields
                print_scr(['Group totals:', str(total_cards)+' cards, '+ \
                    str(total_tokens)+' tokens and '+str(total_shields)+ \
                    ' shields.'])
                choice = choose_option('What would you like to do?',
                                       ['Discard three items[null]', 
                                       'Progress to the next event[null]'],
                                       scenario)
                if total_cards < 1 or total_tokens < 1 or total_shields < 1:
                    choice = 1
                if choice == 0:
                    cardplayer = choose_player(players_with_cards)
                    discard(cardplayer)
                    tokenplayer = choose_player(players_with_tokens)
                    discard_token(tokenplayer)
                    shieldplayer = choose_player(players_with_shields)
                    shieldplayer.shields -= 1
                elif choice == 1:
                    ti.move = 'event'
            
        if ti.move == 'event':
            while 1:
                scenario.board.move_marker()
                update_screen(scenario)
                event = scene_event(active_player, scenario, scenario.event,
                                    ring_bearer)
                scenario.event += 1
                if event == 'next':
                    continue
                if event == 'features':
                    scenario.features = False
                break
            if go == 'end':
                print_scr(['You have finished.'])
                break

        elif ti.move == 'player':
            player = choose_player(players, dice_ims[4])
            if player == None:
                sau.move_sauron()
            else:
                player.increase_corruption(2)
                
        elif ti.move == 'bearer':
            ring_bearer.increase_corruption()
            
        elif ti.tile_type == 'activity':
            if ti.name == scenario.noline:
                print_scr(['There is no ['+ti.name+'] line in this scenario',
                           'Choose another line to move'])
                x = 0
                sep = screen_size[0]/(len(scenario.show_tiles)+1)
                for tile in scenario.show_tiles:
                    x += sep
                    tile.rect.centerx = x
                    tile.rect.top = master.rect.bottom + 75
                    screen.blit(tile.image, tile.rect)
                    pygame.display.update(tile.rect)
                chosen_line, right_click = standard_loop(scenario.show_tiles)
                line = chosen_line.move
                
            elif ti.name in scenario.finished_lines:
                print_scr(['That activity line is complete.',
                           'Choose another line to move'])
                x = 0
                sep = screen_size[0]/(len(scenario.show_tiles)+1)
                for tile in scenario.show_tiles:
                    x += sep
                    tile.rect.centerx = x
                    tile.rect.top = master.rect.bottom + 75
                    screen.blit(tile.image, tile.rect)
                    pygame.display.update(tile.rect)
                chosen_line, right_click = standard_loop(scenario.show_tiles)
                line = chosen_line.move
            else:
                line = ti.move

            moveline(active_player, line, scenario)

            if mainline.pos >= mainline.end or scenario.event == 6:
                print 'You have finished.'
                break

            if mainline.pos < mainline.end:
                end_go(scenario, active_player)

            players[a].active = False
            a = a + 1
            if a > len(players)-1:
                a = 0
            active_player = players[a]
            players[a].active = True

        tiles.remove(tiles[0])
        print '\n'

        if mainline.pos >= mainline.end or scenario.event == 6:
            print 'You have finished.'
            break

    # Ring-bearer removes the Ring.
    ring_bearer.ring = False

    # Other end-of-scenario stuff happens if the scenario isn't Mordor.
    if scenario.name != 'Mordor':
        # New Ring-bearer.
        rb = []
        for play in players:
            rb.append(play.tokens[0])

        for r, no in enumerate(rb):
            if no == max(rb):
                new_ring_bearer = players[r]

        if new_ring_bearer == ring_bearer:
            print_scr(['The Ring remains with '+ring_bearer.name])
        else:
            ring_bearer = new_ring_bearer
            print_scr(['The Ring has passed to '+ring_bearer.name+ \
                ', who draws two cards.'])
            draw_hobbit_card(ring_bearer, 2)

        # Life tokens
        for play in players:
            print play.name, ', you have', play.tokens[0], 'ring tokens,', play.tokens[1], 'heart tokens and', play.tokens[2], 'sun tokens.'
            
            # Athelas
            yn = None
            for pl in players:
                if athelas in pl.hand and (play.tokens[0] < 1 or play.tokens[1] < 1 or play.tokens[2] < 1):
                    ath_pl = pl
                    yn = raw_input('One of you has the Athelas card. You may use this to ignore the effects of missing life tokens. Would you like to do this? [y/n]    ')

            if yn == 'y':
                print 'You have ignored the effects of missing life tokens.\n'
                ath_pl.hand.remove(athelas)
                continue

            toks = 0
            for t in play.tokens:
                if t > 0:
                    toks = toks + 1

            if play == me:
                toks = toks + 1

            if toks < 3:
                hob_corr(play, 3-toks)
                print 'You have been moved on the corruption line for having insufficient life tokens.\n'

            # Reset life tokens.
            play.tokens = [0, 0, 0]

        # Fatty.
        if fa in players:
            print_scr(['Fatty recieves two Hobbit cards at the end of each '+ \
                'scenario.'])
            draw_hobbit_card(fa, 2)

        return ring_bearer

    else:
        print_scr(['------------------------',
                   '|      Mount Doom      |',
                   '------------------------'])

        print_scr(['The Active player must now attempt to destroy the Ring.',
                   'You must roll the dice.'])
        while 1:
            dice(active_player, doom=True)

            if active_player in players:
                print_scr(['Congratulations!',
                           'You have destroyed the Ring and brought peace '+ \
                           'to Middle-Earth',
                           'Take a short holiday'])
                break
            else:
                print_scr(['Oh no! '+active_player.name+' has died.',
                           'Now the next player must attempt to destroy the '+ \
                           'Ring by rolling the dice.'])
                a = a + 1
                active_player = players[a]

            if players == []:
                print_scr(['Damn!',
                           'Every member of the group has died trying to '+ \
                           'destroy the Ring',
                           'Now Sauron has it and evil will devour the '+ \
                           'lands of Middle-Earth'])
                print_scr(['Better luck next time'])
                break
