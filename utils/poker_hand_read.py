import numpy as np


def gg_hero_c_focus(hand):
    
    '''
    Info order:

    hand_id, card, date, time, position, currency, rake, jackpot, premium
    '''
    
    hand_id = hand[0].split(' ')[2].replace('#', '').replace(':', '')
     
    for j in range(2, 8):
        if 'Hero' in hand[j]:
            position = j - 1
            chip = hand[j]
            chip = chip.split(' ')[-3].split('$')[-1]
            chip = float(chip)
            break
        
    small_blind = hand[0].split(' ')[-4]
    small_blind = small_blind.split('$')[-1].replace(')', '')
    small_blind = float(small_blind) / 2
    small_blind = np.around(small_blind, 2)
    
    card = hand[10 + position]
    card = card.split('[')[-1].replace(']', '')
    date = hand[0].split(' ')[-2]
    time = hand[0].split(' ')[-1]
    
        
    result_line = hand[-7 + position]
    
    rake = 0
    jackpot = 0
    
    for j in range(-8, -6):
        if 'Total' in hand[j]:
            
            pot_line = hand[j]
            
            rake = pot_line.split('|')[1]
            rake = rake.split('$')[-1]
            rake = rake.replace(' ', '')
            rake = float(rake)
            
            jackpot = pot_line.split('|')[2]
            jackpot = jackpot.split('$')[-1]
            jackpot = jackpot.replace(' ', '')
            jackpot = float(jackpot)
            
            break
    
    pot = 0
    skip_flag = False
    
    if 'folded before Flop' in result_line:
        
        if 'small blind' in result_line:
            invest = small_blind
        elif 'big blind' in result_line:
            invest = 2 * small_blind
        else:
            invest = 0
        
        premium = 0
        skip_flag = True
        
    elif 'collected' in result_line or 'won' in result_line:
        if 'Premium' not in result_line:
            
            pot = result_line.split('$')[-1].split(')')[0]
            pot = float(pot)
            premium = 0
            
        elif 'Premium' in result_line:
            pot = result_line.split('$')[-2].split(')')[0]
            pot = float(pot)
            premium = result_line.split('$')[-1].split(')')[0]
            premium = float(premium)
            
    else:
        premium = 0
            
    if skip_flag == False:
        
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
            elif '*** SHOWDOWN ***' in line:
                hold_flag = False
                flop_flag = False
                turn_flag = False
                river_flag = False
                break
            
        hole_action = hole_action[::-1]
        flop_action = flop_action[::-1]
        turn_action = turn_action[::-1]
        river_action = river_action[::-1]
        
        if position == 1:
            invest = small_blind
        elif position == 2:
            invest = 2 * small_blind
        else:
            invest = 0
            
        while True:
            
            for line in hole_action:
                if 'Hero' in line:
                    if 'all-in' in line:
                        invest += float(line.split('$')[-1].split(' ')[0])
                    
                    elif 'raises' in line or 'bets' in line or 'calls' in line:
                        invest += float(line.split('$')[-1])
                        invest = np.around(invest, 2)
                        
                    elif 'Uncalled bet' in line:
                        invest -= float(line.split('$')[-1].split(')')[0])
                        invest = np.around(invest, 2)
                    
            for line in flop_action:
                if 'Hero' in line:
                    if 'all-in' in line:
                        invest += float(line.split('$')[-1].split(' ')[0])
                    
                    elif 'raises' in line or 'bets' in line or 'calls' in line:
                        invest += float(line.split('$')[-1])
                        invest = np.around(invest, 2)
                        
                    elif 'Uncalled bet' in line:
                        invest -= float(line.split('$')[-1].split(')')[0])
                        invest = np.around(invest, 2)
                    
            for line in turn_action:
                if 'Hero' in line:
                    if 'all-in' in line:
                        invest += float(line.split('$')[-1].split(' ')[0])
                    
                    elif 'raises' in line or 'bets' in line or 'calls' in line:
                        invest += float(line.split('$')[-1])
                        invest = np.around(invest, 2)
                        
                    elif 'Uncalled bet' in line:
                        invest -= float(line.split('$')[-1].split(')')[0])
                        invest = np.around(invest, 2)
                    
            for line in river_action:
                if 'Hero' in line:
                    if 'all-in' in line:
                        invest += float(line.split('$')[-1].split(' ')[0])
                    
                    elif 'raises' in line or 'bets' in line or 'calls' in line:
                        invest += float(line.split('$')[-1])
                        invest = np.around(invest, 2)
                        
                    elif 'Uncalled bet' in line:
                        invest -= float(line.split('$')[-1].split(')')[0])
                        invest = np.around(invest, 2)
                        
            break
    
    if pot == 0 or skip_flag == True:
        
        rake = 0
        jackpot = 0
    
    profit = pot - invest
    profit = np.around(profit, 2)
        
    return hand_id, card, date, time, position, profit, rake, jackpot, premium
            
            



def gg_read_hand(hand_file):
    
    """
    hand - file_path, which contains poker hands
    """
    
    file_name = hand_file.split('/')[-1]
    file_name = file_name.replace(' ', '')
    file_element = file_name.split('-')
    
    level = int(float(file_element[4]) * 100)
    big_blind = float(file_element[4])
    
    if 'RushAndCash' in file_element[2]:
        game_type = f'zoom NL{level}$'
    
    elif 'PLO' in file_element[2]:
        game_type = f'PLO{level}$'
        
    elif 'NL' in file_element[2]:
        game_type = f'NL{level}$'
    
    hands = []

    with open(hand_file, 'r') as file:
        
        file_content = file.read()
        
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
    rake_list = []
    profit_list = []
    position_list = []
    jackpot_list = []
    premium_list = []
    
    for hand in hands:
        
        while True:
            if hand[-1] == '':
                hand.pop()
            else:
                break
        
        hand_id, card, date, time, position, profit, rake, jackpot, premium = gg_hero_c_focus(hand)
            
        hand_id_list.append(hand_id)
        card_list.append(card)
        date_list.append(date)
        time_list.append(time)
        position_list.append(position)
        profit_list.append(profit)
        rake_list.append(rake)
        jackpot_list.append(jackpot)
        premium_list.append(premium)
        
    
    
    profit_list = np.array(profit_list)
    if any(profit_list != 0):
        profit_list = np.around(profit_list, 2)
    
    rake_list = np.array(rake_list)
    if any(rake_list != 0):
        rake_list = np.around(rake_list, 2)
    
    jackpot_list = np.array(jackpot_list)
    if any(jackpot_list != 0):
        jackpot_list = np.around(jackpot_list, 2)
    
    premium_list = np.array(premium_list)
    if any(premium_list != 0):
        premium_list = np.around(premium_list, 2)
    
    # session_c = sum(currency_list)
    # start_date = date_list[-1]
    # start_time = time_list[-1]
    # end_date = date_list[0]
    # end_time = time_list[0]
    
    return game_type, big_blind, hands, hand_id_list, card_list, date_list, time_list, position_list, profit_list, rake_list, jackpot_list, premium_list
        
    