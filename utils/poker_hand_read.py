def gg_hero_c_focus(hand):
     
    for j in range(2, 8):
        if 'Hero' in hand[j]:
            position = j - 1
            chip = hand[j]
            chip = chip.split(' ')[-3].split('$')[-1]
            chip = float(chip)
            break
        
    small_blind = hand[0].split(' ')[-4]
    small_blind = small_blind.split('$')[-1].replace(')', '')
    small_blind = float(small_blind)
        
    result_line = hand[-7 + position]
    
    if 'folded before Flop' in result_line:
        
        if 'small blind' in result_line:
            return -small_blind
        elif 'big blind' in result_line:
            return -2 * small_blind
        else:
            return 0
        
    elif 'collected' in result_line:
        
        c = result_line.split('$')[-1].split(')')[0]
        c = float(c)
        return c
    
    else:
        
        hole_action = []
        flop_action = []
        turn_action = []
        river_action = []
        
        hold_flag = False
        flop_flag = False
        turn_flag = False
        river_flag = False
        
        for line in hand:
            
            if hold_flag:
                hole_action.append(line)
            elif flop_flag:
                flop_action.append(line)
            elif turn_flag:
                turn_action.append(line)
            elif river_flag:
                river_action.append(line)
            
            if '*** HOLE CARDS ***' in line:
                hold_flag = True
            elif '*** FLOP ***' in line:
                hold_flag = False
                flop_flag = True
            elif '*** TURN ***' in line:
                flop_flag = False
                turn_flag = True
            elif '*** RIVER ***' in line:
                turn_flag = False
                river_flag = True
            elif '*** SHOW DOWN ***' in line:
                break
            
        hole_action = hole_action[::-1]
        flop_action = flop_action[::-1]
        turn_action = turn_action[::-1]
        river_action = river_action[::-1]
        
        if position == 1:
            c = -small_blind
        elif position == 2:
            c = -2 * small_blind
        else:
            c = 0
        
        while True:
            
            for line in hole_action:
                if 'Hero' in line:
                    if 'fold' in line:
                        return c
                    
                    elif 'all-in' in line:
                        return -chip
                        
                    elif 'raises' in line or 'calls' in line:
                        c += float(line.split('$')[-1])
                        break
                    
                    elif 'checks' in line:
                        pass
                    
            for line in flop_action:
                if 'Hero' in line:
                    if 'fold' in line:
                        return c
                    
                    elif 'all-in' in line:
                        return -chip
                    
                    elif 'raises' in line or 'calls' in line:
                        c -= float(line.split('$')[-1])
                        break
                    
                    elif 'bets' in line:
                        c -= float(line.split('$')[-1])
                        break
                    
                    elif 'checks' in line:
                        pass
                    
            for line in turn_action:
                if 'Hero' in line:
                    if 'fold' in line:
                        return c
                    
                    elif 'all-in' in line:
                        return -chip
                    
                    elif 'raises' in line or 'calls' in line:
                        c -= float(line.split('$')[-1])
                        break
                    
                    elif 'bets' in line:
                        c -= float(line.split('$')[-1])
                        break
                    
                    elif 'checks' in line:
                        pass
                    
            for line in river_action:
                if 'Hero' in line:
                    if 'fold' in line:
                        return c
                    
                    elif 'all-in' in line:
                        return -chip
                    
                    elif 'raises' in line or 'calls' in line:
                        c -= float(line.split('$')[-1])
                        break
                    
                    elif 'bets' in line:
                        c -= float(line.split('$')[-1])
                        break
                    
                    elif 'checks' in line:
                        pass
                    
            break
        
        return c
            
            



def gg_read_hand(hand_file):
    
    """
    hand - file_path, which contains poker hands
    """
    
    file_name = hand_file.split('/')[-1]
    file_name = file_name.replace(' ', '')
    file_element = file_name.split('-')
    
    level = int(float(file_element[4]) * 100)
    
    if 'RushAndCash' in file_element[2]:
        game_type = f'zoom NL{level}$'
    
    elif 'PLO' in file_element[2]:
        game_type = f'PLO{level}$'
        
    elif 'NL' in file_element[2]:
        game_type = f'NL{level}$'
    

    with open(hand_file, 'r') as file:
        
        file_content = file.read()
        hands = []
        
        for line in file_content.split('\n'):
            if 'Poker Hand' in line:
                hands.append([])
                hands[-1].append(line)
            else:
                hands[-1].append(line)
                
    # reverse the hands list
    hands = hands[::-1]
                
    hand_id_list = []
    card_list = []
    time_list = []
    date_list = []
    chip_list = []
    rake_list = []
    c_list = []
    position_list = []
    jackpot_list = []
                
    for i, hand in enumerate(hands):
        
        while True:
            if hand[-1] == '':
                hand.pop()
            else:
                break
        
        hand_id = hand[0].split(' ')[2].replace('#', '')
        date = hand[0].split(' ')[-2]
        time = hand[0].split(' ')[-1]
        position = 0
        
        for j in range(2, 8):
            if 'Hero' in hand[j]:
                position = j - 1
                chip = hand[j]
                chip = chip.split(' ')[-3].split('$')[-1]
                chip = float(chip)
                break
            
        card_line = hand[10 + position]
        card = card_line.split('[')[-1].replace(']', '')
            
        for j in range(-8, -6):
            if 'Total' in hand[j]:
                
                pot_line = hand[j]
                
                pot = pot_line.split('|')[0]
                pot = pot.split('$')[-1]
                pot = pot.replace(' ', '')
                pot = float(pot)
                
                rake = pot_line.split('|')[1]
                rake = rake.split('$')[-1]
                rake = rake.replace(' ', '')
                rake = float(rake)
                
                jackpot = pot_line.split('|')[2]
                jackpot = jackpot.split('$')[-1]
                jackpot = jackpot.replace(' ', '')
                jackpot = float(jackpot)
                
                break
                
                
        result_line = hand[-7 + position]
        if 'folded' or 'lost' in result_line:
            rake = 0
            
        hand_id_list.append(hand_id)
        card_list.append(card)
        date_list.append(date)
        time_list.append(time)
        position_list.append(position)
        chip_list.append(chip)
        rake_list.append(rake)
        jackpot_list.append(jackpot)
        
        
    for i in range(1, len(hands)):
        c_list.append(chip_list[i] - chip_list[i-1])
        
    c_list.append(gg_hero_c_focus(hands[-1]))
    
    session_c = sum(c_list)
    start_date = date_list[-1]
    start_time = time_list[-1]
    end_date = date_list[0]
    end_time = time_list[0]
    
    return hand_id_list, card_list, date_list, time_list, position_list, chip_list, rake_list, jackpot_list, c_list, session_c, start_date, start_time, end_date, end_time, game_type
        
    