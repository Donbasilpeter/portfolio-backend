from typing import Optional
from fastapi import FastAPI
import pymongo
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

#setup the bsecodes
from .set_bsecode import * 
from .api_setup import getdata

app = FastAPI()

origins = [

    "*",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = MongoClient("database",27017)
db = client.portfolio_app
collection = db.bsecode


class code_input(BaseModel):
    name: str


class stock_data(BaseModel):
    script_code :str
    from_date :str
    to_date : str
    
  

@app.post("/getcode")
def read_root(input:code_input):
    x = collection.find({"name" : {"$regex" : input.name.upper()}},{'_id': False} )
    x= list(x)
    x= x[:10]
    return {"data" : x}


@app.post("/data")
def read_root(input:stock_data):
    code = input.script_code
    to_date = input.to_date
    from_date = input.from_date
    data = getdata.api_request(code,from_date,to_date)
    if data["response"] == "TRUE":
        newList = []
        normaliseor = data["pricedata"][0]["price"]
        for x in data["pricedata"]:
            newList.append({"date" : x["date"], "type" : x["type"], "price" :float(x["price"])*100/float(normaliseor)})
    else:
        return data
    data["pricedata"] = newList
    return data


