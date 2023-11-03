import MetaTrader5 as mt5
import json

from decimal import Decimal
from buy_sell_ex_forex_next3 import BUY_SELL


class Pos_Common:

    def __init__(self):
       fileObject = open("login.json", "r")
       jsonContent = fileObject.read()
       aList = json.loads(jsonContent)
       
       self.login = int (aList['login'])
       self.Server = aList['Server'] 
       self.Password = aList['Password'] 
       self.symbol_EURUSD = aList['symbol_EURUSD'] 
       self.decimal_sambol = int (aList['decimal_sambol'] )
    
    def decimal(num , decimal_sambol):
        telo = '0.0'
        for i in range(decimal_sambol - 2):  
          telo = telo + "0"
        telo = telo + "1" 
        telo = float (telo)
        decimal_num = Decimal(str(num))
        rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
        return rounded_num  
    
    def decimal_mov(decimal_sambol):
        x = 1
        for i in range(decimal_sambol):
           x = x * 10
        return x 

    async def common_total(price_in , tp_in , status_pos):

        status_marcket = ''
        if status_pos == 'buy':
            status_marcket = 0

        elif status_pos == 'sell':
            status_marcket = 1    

        positions = mt5.positions_get(symbol = Pos_Common().symbol_EURUSD)
        # print("positions:" , positions) 


        list_ticket_POS = []
        list_type = []
        list_price_start = []
        list_tp = []
        list_price_current = []
        volume = []
        
        list_total_pos1 = []
        list_total_pos2 = []
        list_total_pos3 = []
        list_total_pos4 = []

        candel_num = 0
        status_command = False

        x = 1
        for i in range(Pos_Common().decimal_sambol):
            x = x * 10


        for position in positions:
            status_type = position[5]
            # print("status_type:" , status_type)

            price_open = position.price_open
            tp = position.tp
            command = position.comment

            # print("price_open:" , price_open)
            # print("tp:" , tp)
            # print("command:" , command)
            if command:
                  candel_num = command.split('_')
                  status_command = candel_num[0].isnumeric()
                  print("status_command:" , status_command)
                  if status_command == True:
                     candel_num = int (candel_num[0])
                     print("candel_num:" , candel_num)
                     
                     
            if status_type == status_marcket and tp and price_open != tp and command and status_command == True:
                 
                 list_ticket_POS.append(position[0]) 
                 list_type.append(position[5]) 
                 volume.append(position[9]) 
                 list_price_start.append(position[10]) 
                 list_tp.append(position[12]) 
                 list_price_current.append(position[13]) 


        len_pos = len(list_ticket_POS)
        print("len_pos:" , len_pos) 

        
        for index in range(len_pos):
               
            if index == 0:
               list_total_pos1.append(list_ticket_POS[index])  
               list_total_pos1.append(volume[index])  
               list_total_pos1.append(list_type[index])  
               list_total_pos1.append(list_price_start[index])  
               list_total_pos1.append(list_tp[index])  

            elif index == 1:
               list_total_pos2.append(list_ticket_POS[index])  
               list_total_pos2.append(volume[index])  
               list_total_pos2.append(list_type[index])  
               list_total_pos2.append(list_price_start[index])  
               list_total_pos2.append(list_tp[index]) 

        
        # print("list_ticket_POS:" , list_ticket_POS) 
        # print("volume:" , volume) 
        # print("list_type:" , list_type) 
        # print("list_price_start:" , list_price_start) 
        # print("list_tp:" , list_tp) 
        # print("list_price_current:" , list_price_current) 

        print("list_total_pos1:" , list_total_pos1) 
        print("list_total_pos2:" , list_total_pos2) 

        if list_total_pos1:
             type_pos1 = int(list_total_pos1[2])
        # print("type_pos1:" , type_pos1)
        # print("price_in:" , price_in)
        # print("tp_in:" , tp_in)


        if len_pos == 1 and type_pos1 == 0:
                
                ticket_pos1 = int (list_total_pos1[0])
                # print("ticket_pos1:" , ticket_pos1)

                lot_pos1 = Pos_Common.decimal(list_total_pos1[1] , Pos_Common().decimal_sambol)
                lot_pos1 = float(lot_pos1)
                # print("lot_pos1:" , lot_pos1)

                price_pos1 = Pos_Common.decimal(list_total_pos1[3] , Pos_Common().decimal_sambol)
                price_pos1 = float(price_pos1)
                # print("price_pos1:" , price_pos1)
            
                tp_pos1 = Pos_Common.decimal(list_total_pos1[4] , Pos_Common().decimal_sambol)
                tp_pos1 = float(tp_pos1)
                # print("tp_pos1:" , tp_pos1)

                comp1 = price_in - tp_pos1
                comp1 = comp1 * x
                comp1 = int (comp1)
                # print("comp1:" , comp1)

                if price_in >= tp_pos1 and tp_in >= tp_pos1:
                    print("Buy____11111111111")
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True:
                        return ["buy_update_correction" , tp_pos1 , tp_in , [ticket_pos1]]
                    else:
                        return["No data" , x]

                elif price_in < tp_pos1 and price_in < price_pos1 and tp_in <= price_pos1:
                    print("Buy____22222222222")
                    return ["buy_trade" , tp_in]

                elif price_in < price_pos1 and tp_in > price_pos1 and tp_in < tp_pos1:
                    print("buy____33333333333")   
                    return ["buy_trade_correction" , price_pos1]  

                elif price_in < price_pos1 and tp_in >= tp_pos1:
                    print("buy____44444444444") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True:
                        return ["buy_trade_update_correction" , tp_pos1 , tp_in , price_pos1 , [ticket_pos1]]
                    else:
                        return["No data" , x]

                elif price_in >= price_pos1 and tp_in <= tp_pos1 and price_in < tp_pos1 and tp_in > price_pos1:
                    print("buy____55555555555")  
                    return ["no_trade"] 

                elif price_in >= price_pos1 and tp_in > tp_pos1 and price_in < tp_pos1:
                    print("buy____66666666666")  
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True:
                        return ["buy_update_correction" , tp_pos1 , tp_in , [ticket_pos1]]  
                    else:
                        return["No data" , x]


        elif len_pos == 2 and type_pos1 == 0:

                ticket_pos1 = int (list_total_pos1[0])
                # print("ticket_pos1:" , ticket_pos1)

                ticket_pos2 = int (list_total_pos2[0])
                # print("ticket_pos2:" , ticket_pos2)

                lot_pos1 = Pos_Common.decimal(list_total_pos1[1] , Pos_Common().decimal_sambol)
                lot_pos1 = float(lot_pos1)
                # print("lot_pos1:" , lot_pos1)

                lot_pos2 = Pos_Common.decimal(list_total_pos2[1] , Pos_Common().decimal_sambol)
                lot_pos2 = float(lot_pos2)
                # print("lot_pos2:" , lot_pos2)

                price_pos1 = Pos_Common.decimal(list_total_pos1[3] , Pos_Common().decimal_sambol)
                price_pos1 = float(price_pos1)
                # print("price_pos1:" , price_pos1)

                price_pos2 = Pos_Common.decimal(list_total_pos2[3] , Pos_Common().decimal_sambol)
                price_pos2 = float(price_pos2)
                # print("price_pos2:" , price_pos2)
            
                tp_pos1 = Pos_Common.decimal(list_total_pos1[4] , Pos_Common().decimal_sambol)
                tp_pos1 = float(tp_pos1)
                # print("tp_pos1:" , tp_pos1)

                tp_pos2 = Pos_Common.decimal(list_total_pos2[4] , Pos_Common().decimal_sambol)
                tp_pos2 = float(tp_pos2)
                # print("tp_pos2:" , tp_pos2)

                if price_in < tp_pos2 and tp_in <= price_pos2:
                    print("buy____11111111111") 
                    # x = "sell_true"
                    return ["buy_trade" , tp_in]
                
                elif tp_in < tp_pos2 and tp_in > price_pos2 and price_in < price_pos2:
                    print("buy____22222222222") 
                    return ["buy_trade_correction" , price_pos2]  
                
                elif tp_in <= price_pos1 and tp_in > tp_pos2 and price_in < price_pos2:
                    print("buy____33333333333") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , tp_in )
                    if x == True:
                       return ["buy_trade_update_correction" , tp_pos2 , tp_in , price_pos2 , [ticket_pos2]]
                    
                    else:
                        return["No data" , x]
 
                elif tp_in <= tp_pos2 and price_in >= price_pos2:
                    print("buy____44444444444") 
                    return ["no_trade"] 
                
                elif tp_in > tp_pos2 and tp_in <= price_pos1 and price_in > price_pos2 and price_in < tp_pos2:
                    print("buy____55555555555") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , tp_in )
                    if x == True:
                        return ["buy_update_correction" , tp_pos2 , tp_in , [ticket_pos2]]
                    else:
                        return["No data" , x]
                    
                elif price_in >= tp_pos2 and tp_in <= price_pos1 and price_in < price_pos1:
                    print("buy____66666666666") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , tp_in )
                    if x == True:
                        return ["buy_update_correction" , tp_pos2 , tp_in , [ticket_pos2]]
                    else:
                        return["No data" , x]

                elif price_in < price_pos2 and tp_in <= tp_pos1 and tp_in > price_pos1:
                    print("buy____77777777777")
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1 )
                    if x == True:
                        return ["buy_trade_update_correction" , tp_pos2 , price_pos1 , price_pos2 , [ticket_pos2]]
                    else:
                        return["No data" , x]
                    
                elif price_in < price_pos2 and tp_in > tp_pos1:
                    print("buy____88888888888")
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in)
                    y = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1)
                    if x == True and y == True:
                        return ["buy_trade_update_correction" , [tp_pos1 , tp_pos2] , [tp_in , price_pos1] , price_pos2 , [ticket_pos1 , ticket_pos2]]
                    else:
                        return["No data" , [x , y]]
                    
                elif price_in >= price_pos2 and price_in < tp_pos2 and tp_in > price_pos1 and tp_in <= tp_pos1:
                    print("buy____99999999999")
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1)
                    if x == True:
                        return ["buy_update_correction" , tp_pos2 , price_pos1 , [ticket_pos2]]
                    else:
                        return["No data" , x]
                    
                elif price_in >= tp_pos2 and price_in < price_pos1 and tp_in > price_pos1 and tp_in <= tp_pos1:
                    print("buy____10_10_10_10") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1)
                    if x == True:
                        return ["buy_update_correction" , tp_pos2 , price_pos1 , [ticket_pos2]]
                    else:
                        return["No data" , x]

                elif price_in >= tp_pos2 and price_in < price_pos1 and tp_in > tp_pos1:
                    print("buy____11_11_11_11") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in)
                    y = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1)
                    if x == True and y == True:
                        return ["buy_update_correction" , [tp_pos1 , tp_pos2] , [tp_in , price_pos1] , [ticket_pos1 , ticket_pos2]]
                    else:
                        return["No data" , [x , y]]
                    
                elif price_in >= price_pos1 and tp_in <= tp_pos1:
                    print("buy____12_12_12_12") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1)
                    if x == True:
                        return ["buy_update_correction" , tp_pos2 , price_pos1 , [ticket_pos2] ]
                    else:
                        return["No data" , x]
                    
                elif price_in >= price_pos1 and tp_in > tp_pos1:
                    print("buy____13_13_13_13") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in)
                    y = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1)
                    if x == True and y == True:
                        return ["buy_update_correction" , [tp_pos1 , tp_pos2] , [tp_in , price_pos1] , [ticket_pos1 , ticket_pos2] ]  
                    else:
                        return["No data" , [x , y]]
                    
                elif price_in >= tp_pos1 and tp_in > tp_pos1:
                    print("buy____14_14_14_14") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in)
                    if x == True:
                        return ["buy_update_correction" , tp_pos1 , tp_in , [ticket_pos1]]
                    else:
                        return["No data" , x]
                    
                elif price_in >= price_pos2 and price_in < tp_pos2 and tp_in > tp_pos1:  
                    print("buy____15_15_15_15") 
                    x = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in)
                    y = await BUY_SELL.update_buy(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1)
                    if x == True and y == True:
                        return ["buy_update_correction" , [tp_pos1 , tp_pos2] , [tp_in , price_pos1] , [ticket_pos1 , ticket_pos2]]  
                    else:
                        return["No data" , [x , y]]
             

        elif len_pos == 1 and type_pos1 == 1:
                
                ticket_pos1 = int (list_total_pos1[0])
                # print("ticket_pos1:" , ticket_pos1)

                lot_pos1 = Pos_Common.decimal(list_total_pos1[1] , Pos_Common().decimal_sambol)
                lot_pos1 = float(lot_pos1)
                # print("lot_pos1:" , lot_pos1)

                price_pos1 = Pos_Common.decimal(list_total_pos1[3] , Pos_Common().decimal_sambol)
                price_pos1 = float(price_pos1)
                # print("price_pos1:" , price_pos1)
            
                tp_pos1 = Pos_Common.decimal(list_total_pos1[4] , Pos_Common().decimal_sambol)
                tp_pos1 = float(tp_pos1)
                # print("tp_pos1:" , tp_pos1)


                if price_in <= tp_pos1 and tp_in < tp_pos1:
                    print("Sell____11111111111")
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True:
                        return ["sell_update_correction" , tp_pos1 , tp_in , [ticket_pos1]]
                    else:
                        return["No data" , x]

                elif  price_in > price_pos1 and tp_in >= price_pos1:
                    print("Sell____22222222222") 
                    # x = "sell_true"
                    return ["sell_trade" , tp_in]

                elif price_in > price_pos1 and tp_in < price_pos1 and tp_in > tp_pos1:
                    print("Sell____33333333333")   
                    
                    return ["sell_trade_correction" , price_pos1]    

                elif price_in > price_pos1 and tp_in < tp_pos1:
                    print("Sell____44444444444")  
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True:
                        return ["sell_trade_update_correction" , tp_pos1 , tp_in , price_pos1 , [ticket_pos1]]
                    else:
                        return["No data" , x]

                elif price_in <= price_pos1 and tp_in >= tp_pos1:
                    print("Sell____55555555555")  
                    return "no_trade" 

                elif price_in <= price_pos1 and price_in > tp_pos1 and tp_in < tp_pos1:
                    print("Sell____66666666666")  
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True:
                        return ["sell_update_correction" , tp_pos1 , tp_in , [ticket_pos1]]
                    else:
                        return["No data" , x]


        elif len_pos == 2 and type_pos1 == 1:
                
                ticket_pos1 = int (list_total_pos1[0])
                # print("ticket_pos1:" , ticket_pos1)

                ticket_pos2 = int (list_total_pos2[0])
                # print("ticket_pos2:" , ticket_pos2)

                lot_pos1 = Pos_Common.decimal(list_total_pos1[1] , Pos_Common().decimal_sambol)
                lot_pos1 = float(lot_pos1)
                # print("lot_pos1:" , lot_pos1)

                lot_pos2 = Pos_Common.decimal(list_total_pos2[1] , Pos_Common().decimal_sambol)
                lot_pos2 = float(lot_pos2)
                # print("lot_pos2:" , lot_pos2)

                price_pos1 = Pos_Common.decimal(list_total_pos1[3] , Pos_Common().decimal_sambol)
                price_pos1 = float(price_pos1)
                # print("price_pos1:" , price_pos1)

                price_pos2 = Pos_Common.decimal(list_total_pos2[3] , Pos_Common().decimal_sambol)
                price_pos2 = float(price_pos2)
                # print("price_pos2:" , price_pos2)
            
                tp_pos1 = Pos_Common.decimal(list_total_pos1[4] , Pos_Common().decimal_sambol)
                tp_pos1 = float(tp_pos1)
                # print("tp_pos1:" , tp_pos1)

                tp_pos2 = Pos_Common.decimal(list_total_pos2[4] , Pos_Common().decimal_sambol)
                tp_pos2 = float(tp_pos2)
                # print("tp_pos2:" , tp_pos2)

                if price_in > tp_pos2 and price_in > price_pos2 and tp_in > tp_pos2 and tp_in > price_pos2:
                    print("Sell2____11111111111")
                    return ["sell_trade" , tp_in]
                
                elif price_in > price_pos2 and tp_in < price_pos2 and tp_in  >= tp_pos2 and tp_in > price_pos1:
                    print("Sell2___222222222222")
                    return ["sell_trade_correction" , price_pos2]   
                
                elif price_in > price_pos2 and tp_in < tp_pos2 and tp_in >= price_pos1:
                    print("Sell2___333333333333")
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , tp_in )
                    if x == True:
                        return ["sell_trade_update_correction" , tp_pos2 , tp_in , price_pos2 , [ticket_pos2]]
                    else:
                        return["No data" , x]
                    
                elif price_in <= price_pos2 and tp_in >= tp_pos2:
                    print("Sell2____444444444444")  
                    return ["no_trade"]
                
                elif price_in <= price_pos2 and tp_in < tp_pos2 and tp_in >= price_pos1 and price_in > tp_pos2:
                    print("Sell2____555555555555")
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , tp_in )
                    if x == True:
                        return ["sell_update_correction" , tp_pos2 , tp_in , [ticket_pos2]]
                    else:
                        return["No data" , x]

                elif price_in <= tp_pos2 and tp_in < tp_pos2 and tp_in >= price_pos1:
                    print("Sell2____666666666666")
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , tp_in )
                    if x == True:
                        return ["sell_update_correction" , tp_pos2 , tp_in , [ticket_pos2]]
                    else:
                        return["No data" , x]

                elif price_in > price_pos2 and tp_in >= tp_pos1 and tp_in < price_pos1:
                    print("Sell2____777777777777") 
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1 )
                    if x == True:
                        return ["sell_trade_update_correction" , tp_pos2 , price_pos1 , price_pos2 , [ticket_pos2]]
                    else:
                        return["No data" , x]

                elif price_in > price_pos2 and tp_in < tp_pos1:
                    print("Sell2____888888888888") 
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1 )
                    y = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )

                    if x == True and y == True:
                        return ["sell_trade_update_correction" , [tp_pos2 , tp_pos1] , [price_pos1 , tp_in], price_pos2 ,  [ticket_pos2 , ticket_pos1]]
                    else:
                        return["No data" , [x , y]]

                elif price_in <= price_pos2 and tp_in < price_pos1 and tp_in >= tp_pos1 and price_in > tp_pos2:
                    print("Sell2____999999999999") 
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1 )
                    if x == True:
                        return ["sell_update_correction" , tp_pos2 , price_pos1 , [ticket_pos2]]
                    else:
                        return["No data" , x]
                    
                elif price_in <= price_pos2 and price_in >= tp_pos2 and tp_in < tp_pos1:
                    print("Sell2____100000000000")
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1 )
                    y = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True and y == True:
                        return ["sell_update_correction" , [tp_pos2 , tp_pos1] , [price_pos1 , tp_in] , [ticket_pos2 , ticket_pos1]]
                    else:
                        return["No data" , [x , y]]
                    
                elif price_in <= tp_pos2 and price_in > price_pos1 and tp_in  >= tp_pos1 and tp_in < price_pos1:
                    print("Sell2____11_11_11_11")
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1 )
                    if x == True:
                        return ["sell_update_correction" , tp_pos2 , price_pos1 , [ticket_pos2]]
                    else:
                        return["No data" , x]

                elif price_in <= tp_pos2 and price_in > price_pos1 and tp_in < tp_pos1:
                    print("Sell2____12_12_12_12")
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1 )
                    y = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True:
                        return ["sell_update_correction" , [tp_pos2 , tp_pos1] , [price_pos1 , tp_in] , [ticket_pos2 , ticket_pos1]]
                    else:
                        return["No data" , x]
                    
                elif price_in <= price_pos1 and tp_in >= tp_pos1 and price_in > tp_pos1:    
                    print("Sell2____13_13_13_13")
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1 )
                    if x == True:
                        return ["sell_update_correction" , tp_pos2 , price_pos1 , [ticket_pos2] ]
                    else:
                        return["No data" , x]
                    
                elif price_in <= price_pos1 and price_in > tp_pos1 and tp_in < tp_pos1 and price_in < tp_pos2:
                    print("Sell2____14_14_14_14")    
                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos2 , ticket_pos2 , price_pos1 )
                    y = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True and y == True:
                        return ["sell_update_correction" , [tp_pos2 , tp_pos1] , [price_pos1 , tp_in] , [ticket_pos2 , ticket_pos1]]
                    else:
                        return["No data" , [x , y]]
                    
                elif price_in <= tp_pos1 and tp_in < tp_pos1:
                    print("Sell2____15_15_15_15")  

                    x = await BUY_SELL.update_sell(Pos_Common().symbol_EURUSD , lot_pos1 , ticket_pos1 , tp_in )
                    if x == True:
                        return ["sell_update_correction" , tp_pos1 , tp_in , [ticket_pos1] ]
                    else:
                        return["No data" , x]
