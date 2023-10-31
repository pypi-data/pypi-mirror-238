import MetaTrader5 as mt5
import pandas as pd
import json


class Candel:

    def timecandel(symbol , timestamp ):
    # def timecandel(symbol):
      try:
          timecandel = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M15, timestamp, 25)
        #   timecandel = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 25)
        #   timecandel = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 24)

          return timecandel
      except:
          return False
      
    def candelstate(x , listOpen , listClose):
         candel_open = listOpen[x]
         candel_close = listClose[x]
        #  candel_open = Candel.decimal(candel_open)
        #  candel_close = Candel.decimal(candel_close)
        #  print("candel_open" , candel_open) 
        #  print("candel_close" , candel_close) 
         if candel_open > candel_close:
             candel_state = "red"
     
         elif candel_open < candel_close:
             candel_state = "green"
                 
         elif candel_open == candel_close:
             candel_state = "doji"
     
         return candel_state     


class Timecandel:
   
   def time_candel_timestamp(symbol_EURUSD , timestamps):   


        timecandel = Candel.timecandel(symbol_EURUSD , timestamps)

        # print("timecandel:" , timecandel)
        

        # timecandel = Candel.timecandel(symbol_EURUSD )
        
        # print("timcandel:", timecandel)
        # timestamp = timecandel[24][0]
        # timestamp = int (timestamp)
        
        # timecandel_mine = mt5.copy_rates_from(symbol_EURUSD, mt5.TIMEFRAME_M1, timestamp , 361)
        

        listtimess = []
        listTimestamp = []
        listOpen = []
        listHigh = []
        listLow = []
        listClose = []
        
        for item in timecandel:
                     listtimess.append(pd.to_datetime( item[0] , unit='s'))
                     listTimestamp.append(item[0])
                     listOpen.append(item[1])
                     listHigh.append(item[2])
                     listLow.append(item[3])
                     listClose.append(item[4])
        
        dictdata = {'Timestamp':listTimestamp , 'listtimess':listtimess ,'Open':listOpen ,'High':listHigh ,'Low':listLow ,'Close':listClose}             
        df = pd.DataFrame(dictdata,columns=['Timestamp', 'listtimess' ,'Open','High','Low','Close'])
        # print(df)
        listtimess = []
        listTimestamp = []
        listOpen = []
        listHigh = []
        listLow = []
        listClose = []
        
        json_data = df.to_json()
        
        # print(json_data)
        aList = json.loads(json_data)
        listtimesss = aList["listtimess"]
        listTime = aList["Timestamp"]
        close = aList["Close"]
        open = aList["Open"]
        high = aList["High"]
        low = aList["Low"]
        
        for index in range(25):
                listtimess.append(listtimesss[f'{index}'])
                listTimestamp.append(listTime[f'{index}'])
                listClose.append(close[f'{index}'])
                listOpen.append(open[f'{index}'])
                listLow.append(low[f'{index}'])
                listHigh.append(high[f'{index}'])
        
        
        prices = pd.DataFrame(dictdata)
        prices.to_json(orient = 'columns')

        # print ("listClose:" , listClose)
        
        df = pd.DataFrame(prices)  
        # write dataframe to csv
        # df.to_csv('output.csv', index = True, header = True) 


        return [timecandel , listOpen , listClose , listTimestamp ]