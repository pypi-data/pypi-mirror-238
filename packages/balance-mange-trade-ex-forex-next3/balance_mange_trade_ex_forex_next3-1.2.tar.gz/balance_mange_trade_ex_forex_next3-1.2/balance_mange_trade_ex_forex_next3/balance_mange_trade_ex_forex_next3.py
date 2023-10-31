import MetaTrader5 as mt5
import pandas as pd
import json

from decimal import Decimal

class Manage_balance_trade:
      
      def __init__(self):
           fileObject = open("login.json", "r")
           jsonContent = fileObject.read()
           aList = json.loads(jsonContent)

           self.max_lot_balance_manage = float(aList['max_lot_balance_manage'])

           self.list_crypto_trade_balance = aList['list_crypto_trade_balance'] 
           self.list_crypto_trade_balance_decimal = aList['list_crypto_trade_balance_decimal'] 
           
      def decimal(num , decimal_sambol):
           telo = '0.0'
           for i in range(decimal_sambol - 2):  
             telo = telo + "0"
           telo = telo + "1" 
           telo = float (telo)
           decimal_num = Decimal(str(num))
           rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
           return rounded_num  
    
      def balance_candel( input_lot , input_type , input_symbul):   

           list_balance1 = []
           list_balance2 = []

           list_crypto_p = []
           list_crypto_n = []

           
           for index , index_balance in enumerate(Manage_balance_trade().list_crypto_trade_balance):      
             
            #  print("index_balance:" , index_balance)
           
             rec_manage_balance_trade = mt5.copy_rates_from_pos(index_balance, mt5.TIMEFRAME_M15, 1, 24)
            #  print("rec_manage_balance_trade:" , rec_manage_balance_trade)

             decimal_sambol_balance = Manage_balance_trade().list_crypto_trade_balance_decimal[index]
            #  print("decimal_sambol_balance:" , decimal_sambol_balance)
             decimal_sambol_balance = int(decimal_sambol_balance)

             price_close_start = rec_manage_balance_trade[23][4]
             price_close_start = Manage_balance_trade.decimal(price_close_start , decimal_sambol_balance)
             price_close_start = float(price_close_start)
            #  print("price_close_start:" , price_close_start)

             price_close_end = rec_manage_balance_trade[0][4]
             price_close_end = Manage_balance_trade.decimal(price_close_end , decimal_sambol_balance)
             price_close_end = float(price_close_end)
            #  print("price_close_end:" , price_close_end)

             x = 1
             for i in range(decimal_sambol_balance):
              x = x * 10
              
             result = price_close_start - price_close_end
             result = result * x
            #  print("result:" , result )
             result = round(result)
             result = int(result)
            #  print("result:" , result )

             if result > 0:
                #  print("index_balance:" , index_balance)
                 list_balance1.append([index_balance , result])
                 list_crypto_p.append(index_balance)
             elif result < 0:
                #  print("index_balance:" , index_balance) 
                 list_balance2.append([index_balance , result])
                 list_crypto_n.append(index_balance)
                 

            #  print("")
           
            
        #    print("list_balance1:" , list_balance1)
        #    print("list_balance2:" , list_balance2)

        #    print("list_crypto_p:" , list_crypto_p)
        #    print("list_crypto_n:" , list_crypto_n)
 

           list_lot_p_buy = []
           list_symbol_P_buy = []

           list_lot_p_sell = []
           list_symbol_P_sell = []

           list_lot_n_buy = []
           list_symbol_n_buy = []

           list_lot_n_sell = []
           list_symbol_n_sell = []

           list_position_symbul = []

           positions = mt5.positions_get()
        #    print("positions:" , positions)
           
           for i_list_symbul in positions:
               list_position_symbul.append(i_list_symbul[16])


        #    print("")   
        #    print("list_position_symbul:" , list_position_symbul) 
           

           for index_pos in positions:
               
               for index_symbol in list_crypto_p:
                   if index_pos[16] == index_symbol and index_pos[5] == 0:
                    #    print("111111111111111111111111111")
                    #    print("symbol:" , index_symbol)
                       list_lot_p_buy.append(index_pos[9])
                       list_symbol_P_buy.append(index_pos[16])

                   if index_pos[16] == index_symbol and index_pos[5] == 1:
                    #    print("22222222222222222222222222")
                    #    print("symbol:" , index_symbol)
                       list_lot_p_sell.append(index_pos[9])
                       list_symbol_P_sell.append(index_pos[16])

               for index_symbol in list_crypto_n:
                   if index_pos[16] == index_symbol and index_pos[5] == 0:
                    #    print("111111111111111111111111111")
                    #    print("symbol:" , index_symbol)
                       list_lot_n_buy.append(index_pos[9])
                       list_symbol_n_buy.append(index_pos[16])

                   if index_pos[16] == index_symbol and index_pos[5] == 1:
                    #    print("22222222222222222222222222")
                    #    print("symbol:" , index_symbol)
                       list_lot_n_sell.append(index_pos[9])
                       list_symbol_n_sell.append(index_pos[16])        
                           

        #    print("")
        #    print("list_lot_p_buy:" , list_lot_p_buy)   
        #    print("list_symbol_P_buy:" , list_symbol_P_buy)  
        #    print("")

        #    print("list_lot_p_sell:" , list_lot_p_sell)   
        #    print("list_symbol_P_sell:" , list_symbol_P_sell)    

        #    print("")
        #    print("")

        #    print("list_lot_n_buy:" , list_lot_n_buy)   
        #    print("list_symbol_n_buy:" , list_symbol_n_buy)  
        #    print("")

        #    print("list_lot_n_sell:" , list_lot_n_sell)   
        #    print("list_symbol_n_sell:" , list_symbol_n_sell) 
        #    print("") 
           add_list_lot = 0

           if input_type == 'buy':
               
               for index_t in list_balance1:
                   if index_t[0] == input_symbul:
                       print("input_symbul_+:" , input_symbul)
                       
                       for i_p in list_lot_p_buy:
                           add_list_lot = i_p + add_list_lot

                       for i_p in list_lot_n_sell:
                           add_list_lot = i_p + add_list_lot

                       add_list_lot = round(add_list_lot , 2)     
                           

               for index_t in list_balance2:
                   if index_t[0] == input_symbul:
                       print("input_symbul_-:" , input_symbul)
                       
                       for i_p in list_lot_n_buy:
                           add_list_lot = i_p + add_list_lot

                       for i_p in list_lot_p_sell:
                           add_list_lot = i_p + add_list_lot

                       add_list_lot = round(add_list_lot , 2)


           elif input_type == 'sell':
               print("sell")
               
               for index_t in list_balance1:
                   if index_t[0] == input_symbul:
                       print("input_symbul ++:" , input_symbul)

                       for i_p in list_lot_p_sell:
                           add_list_lot = i_p + add_list_lot

                       for i_p in list_lot_n_buy:
                           add_list_lot = i_p + add_list_lot

                       add_list_lot = round(add_list_lot , 2)     
                           

               for index_t in list_balance2:
                   if index_t[0] == input_symbul:
                       print("input_symbul ---:" , input_symbul)

                       for i_p in list_lot_n_sell:
                           add_list_lot = i_p + add_list_lot

                       for i_p in list_lot_p_buy:
                           add_list_lot = i_p + add_list_lot

                       add_list_lot = round(add_list_lot , 2)
 
        #    print("add_list_lot:" , add_list_lot) 

           result_lot =  add_list_lot + input_lot
        #    print("result_lot:" , result_lot)

           if result_lot <= Manage_balance_trade().max_lot_balance_manage:
            #    print("ooooooooooooooooooooooooooooooooooooooook")  
               return False 
           elif result_lot > Manage_balance_trade().max_lot_balance_manage:
               return True
           
           else:
               return None
