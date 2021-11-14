import requests
import json

class getdata:
    def __init__(self):
        self.data = []
    
    def api_request(code,from_date,to_date):
        api_url = 'https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w?scripcode=' + code + '&flag=1&fromdate=' + from_date + '&todate=' + to_date +  '&seriesid='
        response = requests.get(api_url, headers={'User-Agent' : ''})
        responsedata = json.loads(response.content)
        name = responsedata["Scripname"]
        responsedata = responsedata["Data"]
        responsedata =json.loads(responsedata)
        return responsedata
                
