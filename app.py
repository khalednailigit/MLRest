from flask import Flask, request
from flask_restful import Resource, Api
import pickle
import pandas as pd
from flask_cors import CORS
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

app = Flask(__name__)
#
CORS(app)
# create an API object
api = Api(app)
#predection api call

class prediction(Resource):
    def get(self,valueInCurrency,valueToReimburse,VatAvgRate,currency,dayInvoice,hourInvoice,dayCreation,hourCreation,Name_EN,merchantCountry,merchantCity,hasPhoto,MerchantName,Source):
        #budget = request.args.get('budget')
        print(valueInCurrency, valueToReimburse, VatAvgRate, currency, dayInvoice, hourInvoice, dayCreation, hourCreation, Name_EN, merchantCountry, merchantCity, hasPhoto, MerchantName, Source)

        invoice = [(valueInCurrency), (valueToReimburse), (VatAvgRate), (currency), (dayInvoice), (hourInvoice), (dayCreation), (hourCreation), (Name_EN), (merchantCountry), (merchantCity), (hasPhoto), (MerchantName), (Source)]
        #1.20&1.20&20.000000&15&5&13&5&14&1272&24&1735&0&2380&13.0
        staticInvoice = [1.20,1.20,20.000000,15,5,13,5,14,1272,24,1735,0,2380,13.0]
       #Index(['valueInCurrency', 'valueToReimburse', 'VatAvgRate', 'currency', 'dayInvoice', 'hourInvoice', 'dayCreation', 'hourCreation', 'Name_EN', 'merchantCountry', 'merchantCity', 'hasPhoto', 'MerchantName', 'Source'], dtype='object')
        df = pd.DataFrame(staticInvoice,dtype='object')
       
        
        
        print(df.shape)
        model = pickle.load(open('model.pkl', 'rb'))
        prediction = model.predict(df)
        prediction = int(prediction[0])
        return str(prediction)

#data api
class getData(Resource):
    def get(self):
        df = pd.read_csv('invoices.csv', on_bad_lines='skip')
        #df = df.rename({'Marketing Budget':'budget','Actual Sales':'Sales'},axis=1)
        #print(df.head())
        #out = {'Key': 'str'}
        res = df.to_json(orient='records')
        return res

api.add_resource(getData, '/api')
#valueInCurrency;valueToReimburse;VatAvgRate;currency;dayInvoice;hourInvoice;dayCreation;hourCreation;Name_EN;merchantCountry;merchantCity;hasPhoto;MerchantName;Source
api.add_resource(prediction, '/prediction/<string:valueInCurrency>/<string:valueToReimburse>/<string:VatAvgRate>/<string:currency>/<string:dayInvoice>/<string:hourInvoice>/<string:dayCreation>/<string:hourCreation>/<string:Name_EN>/<string:merchantCountry>/<string:merchantCity>/<string:hasPhoto>/<string:MerchantName>/<string:Source>')