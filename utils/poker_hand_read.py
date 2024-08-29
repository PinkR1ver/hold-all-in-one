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
                
    for i, hand in enumerate(hands):
        
        if i == 0:
            line = hand[0]
            line = line.split(' ')
            end_date = line[-2]
            end_time = line[-1]
            
        if i == len(hands) - 1:
            line = hand[0]
            line = line.split(' ')
            start_date = line[-2]
            start_time = line[-1]
        
        hand_id = hand[0].split(' ')[2].replace('#', '')
        
            
    return game_type, start_date, start_time, end_date, end_time, hands