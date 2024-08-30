import os
import numpy as np
import matplotlib.pyplot as plt



def all_time_report(data_path):
    
    profit_c_list = []
    rake_c_list = []
    jackpot_c_list = []
    premium_c_list = []
    
    profit_bb_list = []
    rake_bb_list = []
    jackpot_bb_list = []
    premium_bb_list = []
    
    for root, dirs, files in os.walk(data_path):
        
        for file in files:
            
            if 'currency.txt' in file:
                
                with open(os.path.join(root, file), 'r') as f:
                    
                    currency = f.read()
                    for i, line in enumerate(currency.split('\n')):
                        
                        if i == len(currency.split('\n')) - 1:
                            break
                        
                        else:
                            profit_c = float(line.split(' ')[3].replace('$', ''))
                            rake_c = float(line.split(' ')[6].replace('$', ''))
                            jackpot_c = float(line.split(' ')[9].replace('$', ''))
                            premium_c = float(line.split(' ')[12].replace('$', ''))
                            
                            profit_bb = float(line.split(' ')[4].replace('bb', ''))
                            rake_bb = float(line.split(' ')[7].replace('bb', ''))
                            jackpot_bb = float(line.split(' ')[10].replace('bb', ''))
                            premium_bb = float(line.split(' ')[13].replace('bb', ''))
                            
                            profit_c_list.append(profit_c)
                            rake_c_list.append(rake_c)
                            jackpot_c_list.append(jackpot_c)
                            premium_c_list.append(premium_c)
                            
                            profit_bb_list.append(profit_bb)
                            rake_bb_list.append(rake_bb)
                            jackpot_bb_list.append(jackpot_bb)
                            premium_bb_list.append(premium_bb)
                            
                            
    fig = plt.figure(figsize=(12, 6))
    plt.plot(np.cumsum(profit_c_list) + jackpot_c_list, label='Profit')
    plt.plot(np.cumsum(rake_c_list), label='Rake')
    plt.plot(np.cumsum(jackpot_c_list), label='Jackpot')
    # plt.plot(np.cumsum(premium_c_list), label='Premium')
    plt.xlabel('Hands')
    plt.ylabel('USD $')
    plt.legend()
    plt.grid()
    plt.title('Profit Fluctuation Curve')
    
    fig.subplots_adjust(left=0.3)
    
    fig.text(0.05, 0.65, f'Profit: {np.round(np.sum(profit_c_list), 2)} + {np.round(np.sum(jackpot_c_list), 2)}$', color='blue', fontsize=15)
    fig.text(0.05, 0.6, f'Rake: {np.round(np.sum(rake_c_list), 2)}$', color='orange', fontsize=15)
    fig.text(0.05, 0.55, f'Jackpot: {np.round(np.sum(jackpot_c_list), 2)}$', color='green', fontsize=15)
    fig.text(0.05, 0.5, f'Premium: {np.round(np.sum(premium_c_list), 2)}$', color='red', fontsize=15)
    fig.text(0.05, 0.45, f'Real Rake: {np.round(np.sum(rake_c_list) - np.sum(jackpot_c_list), 2)}$', color='black', fontsize=15)
    fig.text(0.05, 0.4, f'P/100: {np.round((np.sum(profit_c_list) + np.sum(jackpot_c_list)) / len(profit_c_list) * 100, 2)}$', color='purple', fontsize=15)
    fig.text(0.05, 0.35, f'P/100 bb: {np.round((np.sum(profit_bb_list) + np.sum(jackpot_bb_list)) / len(profit_bb_list) * 100, 2)}bb', color='brown', fontsize=15)

    
    
    plt.show()
        
                
                
                
if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, '..', 'data', 'psych0W')
    all_time_report(data_path)