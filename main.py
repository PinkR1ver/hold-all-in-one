from utils.utils import *
import tkinter as tk
import tkinter.filedialog as fd
import os

script_path = os.path.dirname(__file__)
data_path = os.path.join(script_path, 'data')


if __name__ == '__main__':
    
    hero_name = input('Enter hero name: ')
    if hero_name == '':
        hero_name = 'default'
    
    hero_data_path = os.path.join(data_path, hero_name)
    if not os.path.exists(hero_data_path):
        os.mkdir(hero_data_path)
        
    while True:
        
        print('1. Build hero database')
        print('2. Show the Report')
        print('3. Exit')
        
        choice = input('Enter your choice: ')
        
        if choice == '1':
            
            #input lots of files in one time
            hand_files = fd.askopenfilenames()
            for hand_file in hand_files:
                hand_id_list, card_list, date_list, time_list, position_list, chip_list, rake_list, jackpot_list, c_list, session_c, start_date, start_time, end_date, end_time, game_type, hands = gg_read_hand(hand_file)
                
                for i in range(len(hand_id_list)):
                    hand_id = hand_id_list[i]
                    card = card_list[i]
                    date = date_list[i]
                    time = time_list[i]
                    position = position_list[i]
                    chip = chip_list[i]
                    rake = rake_list[i]
                    jackpot = jackpot_list[i]
                    c = c_list[i]
                    hand = hands[i]
                    
                    year = date.split('/')[0]
                    month = date.split('/')[1]
                    day = date.split('/')[2]
                    
                    if not os.path.exists(os.path.join(hero_data_path, year)):
                        os.mkdir(os.path.join(hero_data_path, year))
                    if not os.path.exists(os.path.join(hero_data_path, year, month)):
                        os.mkdir(os.path.join(hero_data_path, year, month))
                    if not os.path.exists(os.path.join(hero_data_path, year, month, day)):
                        os.mkdir(os.path.join(hero_data_path, year, month, day))
                        
                    hand_path = os.path.join(hero_data_path, year, month, day, hand_id + '.txt')
                    with open(hand_path, 'w') as f:
                        f.write(hand)
                        
                    currency_path = os.path.join(hero_data_path, year, month, day, 'currency.txt')
                    with open(currency_path, 'r') as f:
                        currency = f.read()
                        
                    
                    
                    
            
        elif choice == '2':
            pass
        
        elif choice == '3':
            exit()
        
        else:
            print('Invalid choice. Pls input again')
        
        
    