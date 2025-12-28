from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["GorevTakipProje"]
kullanicilar_col = db["kullanicilar"]  


veri=MongoClient("mongodb://localhost:27017/")
dbb=veri["GorevTakipProje"]
gorev=dbb["gorevler"]