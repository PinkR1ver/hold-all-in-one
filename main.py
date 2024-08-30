from utils.utils import *
import tkinter.filedialog as fd
import os
import numpy as np

script_path = os.path.dirname(__file__)
data_path = os.path.join(script_path, 'data')


if __name__ == '__main__':
    
    print('----------------------------------------')
    print('Welcome to Hold\'em All-in-One')
    print('\n\n')
    
    hero_name = input('Enter hero name: ')
    if hero_name == '':
        hero_name = 'default'
    
    hero_data_path = os.path.join(data_path, hero_name)
    if not os.path.exists(hero_data_path):
        os.mkdir(hero_data_path)
        
    while True:
        
        print('\n') 
        print('----------------------------------------')
        print('Hello, ' + hero_name)
        print('1. Build hero database')
        print('2. Show the Report')
        print('3. Exit')
        
        choice = input('Enter your choice: ')
        
        if choice == '1':
            
            #input lots of files in one time
            hand_files = fd.askopenfilenames()
            for hand_file in hand_files:
                
                game_type, big_blind, hands, hand_id_list, card_list, date_list, time_list, position_list, profit_list, rake_list, jackpot_list, premium_list = gg_read_hand(hand_file)
                game_type = game_type.replace(' ', '-')
                
                for i in range(len(hand_id_list)):
                    hand_id = hand_id_list[i]
                    card = card_list[i]
                    date = date_list[i]
                    time = time_list[i]
                    position = position_list[i]
                    rake = rake_list[i]
                    jackpot = jackpot_list[i]
                    profit = profit_list[i]
                    premium = premium_list[i]
                    hand = hands[i]
                                  
                    hand_write = ''
                    for line in hand:
                        hand_write += line + '\n'
                    
                    
                    year = date.split('/')[0]
                    month = date.split('/')[1]
                    day = date.split('/')[2]
                    
                    if not os.path.exists(os.path.join(hero_data_path, game_type)):
                        os.mkdir(os.path.join(hero_data_path, game_type))
                    if not os.path.exists(os.path.join(hero_data_path, game_type, year)):
                        os.mkdir(os.path.join(hero_data_path, game_type, year))
                    if not os.path.exists(os.path.join(hero_data_path, game_type, year, month)):
                        os.mkdir(os.path.join(hero_data_path, game_type, year, month))
                    if not os.path.exists(os.path.join(hero_data_path, game_type, year, month, day)):
                        os.mkdir(os.path.join(hero_data_path, game_type, year, month, day))
                        
                    save_path = os.path.join(hero_data_path, game_type, year, month, day)
                        
                    currency_path = os.path.join(save_path, 'currency.txt')
                    if not os.path.exists(currency_path):
                        with open(os.path.join(save_path, 'currency.txt'), 'w') as f:
                            f.write('profit 0$ 0bb rake 0$ 0bb jackpot 0$ 0bb premium 0$ 0bb')
                            f.close()
                        
                    hand_path = os.path.join(save_path, hand_id + '.txt')
                    if not os.path.exists(hand_path):
                        
                        currency_write = ''
                        
                        with open(hand_path, 'w') as f:
                            f.write(hand_write)
                            f.close()
                        
                        with open(currency_path, 'r') as f:
                            currency = f.read()
                            insert_line = hand_id + ' ' + time + ' ' + 'profit ' + str(profit) + '$ ' + str(np.around(float(profit/big_blind), 2)) + 'bb ' + 'rake ' + str(rake) + '$ ' + str(np.around(float(rake/big_blind), 2)) + 'bb ' + 'jackpot ' + str(jackpot) + '$ ' + str(np.around(float(jackpot/big_blind), 2)) + 'bb ' + 'premium ' + str(premium) + '$ ' + str(np.around(float(premium/big_blind), 2)) + 'bb'
                            
                            if '\n' not in currency:
                                currency = [insert_line, currency]
                            
                            else:
                                currency = currency.split('\n')
                                insert_time = parse_time(time)
                                
                                for index_line, line in enumerate(currency):
                                    
                                    if index_line == len(currency) - 1:
                                        currency.insert(index_line, insert_line)
                                        break
                                    
                                    record_time = parse_time(line.split(' ')[1])
                                    if record_time > insert_time:
                                        currency.insert(index_line, insert_line)
                                        break
                                
                            profit_c = currency[-1].split(' ')[1].replace('$', '')
                            profit_bb = currency[-1].split(' ')[2].replace('bb', '')
                            
                            profit_c  = np.around(float(profit_c) + profit, 2)
                            profit_bb = np.around(float(profit_bb) + float(profit/big_blind), 2)
                            
                            rake_c = currency[-1].split(' ')[4].replace('$', '')
                            rake_bb = currency[-1].split(' ')[5].replace('bb', '')
                            
                            rake_c = np.around(float(rake_c) + rake, 2)
                            rake_bb = np.around(float(rake_bb) + float(rake/big_blind), 2)
                            
                            jackpot_c = currency[-1].split(' ')[7].replace('$', '')
                            jackpot_bb = currency[-1].split(' ')[8].replace('bb', '')
                            
                            jackpot_c = np.around(float(jackpot_c) + jackpot, 2)
                            jackpot_bb = np.around(float(jackpot_bb) + float(jackpot/big_blind), 2)
                            
                            premium_c = currency[-1].split(' ')[10].replace('$', '')
                            premium_bb = currency[-1].split(' ')[11].replace('bb', '')
                            
                            premium_c = np.around(float(premium_c) + premium, 2)
                            premium_bb = np.around(float(premium_bb) + float(premium/big_blind), 2)
                            
                            currency[-1] = 'profit ' + str(profit_c) + '$ ' + str(profit_bb) + 'bb ' + 'rake ' + str(rake_c) + '$ ' + str(rake_bb) + 'bb ' + 'jackpot ' + str(jackpot_c) + '$ ' + str(jackpot_bb) + 'bb ' + 'premium ' + str(premium_c) + '$ ' + str(premium_bb) + 'bb'
                                
                            
                            for line in currency:
                                currency_write += line + '\n'
                            
                            currency_write = currency_write[:-1]
                            
                            f.close()
                                
                        with open(currency_path, 'w') as f:
                            f.write(currency_write)
                            f.close()              
                    
            print('Hero database has been built')
            print('----------------------------------------')
            
        elif choice == '2':
            
            print('\n')
            print('----------------------------------------')
            print('1. Show over all currency won')
            print('2. exit')
            
            report_choice = input('Enter your choice: ')
            
            if report_choice == 1:
                
                pass
            
            elif report_choice == 2:
                
                print('Bye!')
                print('----------------------------------------')
        
        elif choice == '3':
            exit()
        
        else:
            print('Invalid choice. Pls input again')
        
        
    