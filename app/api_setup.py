import requests
import json
import datetime

class getdata:
    def __init__(self):
        self.data = []
    
    def api_request(code,from_date,to_date):
        sensex_url = "https://api.bseindia.com/BseIndiaAPI/api/SensexGraphData/w?index=16&flag=1&sector=&seriesid=DT&frd=" + from_date + "&tod=" + to_date
        api_url = 'https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w?scripcode=' + code + '&flag=1&fromdate=' + from_date + '&todate=' + to_date +  '&seriesid='
        response = requests.get(sensex_url, headers={'User-Agent' : ''})
        responsedata = json.loads(response.content)
        responsedata = responsedata.split("#@#",1)[1] 
        sensexdata = json.loads(responsedata)
        response = requests.get(api_url, headers={'User-Agent' : ''})
        responsedata = json.loads(response.content)
        name = responsedata["Scripname"]
        responsedata = responsedata["Data"]
        data =json.loads(responsedata)
        price_data = []
        index = 0
        if sensexdata:
            for sensex_data in sensexdata:
                if data:
                    sensex_date =datetime.datetime.strptime(sensex_data['date'][0:15], '%a %b %d %Y').strftime('%Y-%m-%d')
                    stock_date =datetime.datetime.strptime(data[index]['dttm'][0:15], '%a %b %d %Y').strftime('%Y-%m-%d')
                    if sensex_date == stock_date:
                        price_data.append({"date": sensex_date, "price" :  data[index]["vale1"] ,"type":True})
                        index =index+1
                    else:
                        if index ==0:
                            price_data.append({"date": sensex_date, "price" :  data[index+1]["vale1"] ,"type":False})
                        else:
                            price_data.append({"date": sensex_date, "price" :  data[index-1]["vale1"] ,"type":False})
                
                else:
                    return {"response":"FALSE"}
            price = {"script_code" : code, "name" : name, "pricedata" :price_data,"response":"TRUE"}
            return price
        else:
            return {"response":"FALSE"}
                
