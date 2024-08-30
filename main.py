from utils.utils import *
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
                hand_id_list, card_list, date_list, time_list, position_list, chip_list, rake_list, jackpot_list, c_list, session_c, start_date, start_time, end_date, end_time, game_type, big_blind, hands = gg_read_hand(hand_file)
                
                
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
                    
                    c = np.around(c, 2)
                    rake = np.around(rake, 2)
                    jackpot = np.around(jackpot, 2)
                    
                    
                    hand_write = ''
                    for line in hand:
                        hand_write += line + '\n'
                    
                    
                    year = date.split('/')[0]
                    month = date.split('/')[1]
                    day = date.split('/')[2]
                    
                    if not os.path.exists(os.path.join(hero_data_path, year)):
                        os.mkdir(os.path.join(hero_data_path, year))
                    if not os.path.exists(os.path.join(hero_data_path, year, month)):
                        os.mkdir(os.path.join(hero_data_path, year, month))
                    if not os.path.exists(os.path.join(hero_data_path, year, month, day)):
                        os.mkdir(os.path.join(hero_data_path, year, month, day))
                        
                    currency_path = os.path.join(hero_data_path, year, month, day, 'currency.txt')
                    if not os.path.exists(currency_path):
                        with open(os.path.join(hero_data_path, year, month, day, 'currency.txt'), 'w') as f:
                            f.write('currency: 0$ 0bb')
                            f.close()
                        
                    hand_path = os.path.join(hero_data_path, year, month, day, hand_id + '.txt')
                    if not os.path.exists(hand_path):
                        
                        currency_write = ''
                        
                        with open(hand_path, 'w') as f:
                            f.write(hand_write)
                            f.close()
                        
                        with open(currency_path, 'r') as f:
                            currency = f.read()
                            insert_line = time + ' ' + str(c) + '$ ' + str(np.around(float(c/big_blind), 2)) + 'bb'
                            
                            if '\n' not in currency:
                                currency = [insert_line, currency]
                            
                            else:
                                currency = currency.split('\n')
                                insert_time = parse_time(time)
                                
                                for index_line, line in enumerate(currency):
                                    
                                    if index_line == len(currency) - 1:
                                        currency.insert(index_line, insert_line)
                                        break
                                    
                                    record_time = parse_time(line.split(' ')[0])
                                    if record_time > insert_time:
                                        currency.insert(index_line, insert_line)
                                        break
                                
                                currency_c = currency[-1].split(' ')[1].replace('$', '')
                                currency_bb = currency[-1].split(' ')[2].replace('bb', '')
                                currency_c = np.around(float(currency_c) + c, 2)
                                currency_bb = np.around(float(currency_bb) + float(c/big_blind), 2)
                                currency[-1] = currency[-1].split(' ')[0] + ' ' + str(currency_c) + '$ ' + str(currency_bb) + 'bb'
                                
                            
                            for line in currency:
                                currency_write += line + '\n'
                            
                            currency_write = currency_write[:-1]
                            
                            f.close()
                                
                        with open(currency_path, 'w') as f:
                            f.write(currency_write)
                            f.close()              
                    
            print('\n\n')
            print('Hero database has been built')
            print('----------------------------------------')
            print('\n\n')
            
        elif choice == '2':
            pass
        
        elif choice == '3':
            exit()
        
        else:
            print('Invalid choice. Pls input again')
        
        
    