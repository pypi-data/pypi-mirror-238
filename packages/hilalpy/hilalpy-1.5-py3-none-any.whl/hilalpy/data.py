def data (data_loc):

    from pymongo import MongoClient
    import os,glob, pandas as pd

    
    client = MongoClient("mongodb+srv://userhilalpy:kSTkJBzJ8CbCATmm@hilalpy.wdazfdi.mongodb.net/?retryWrites=true&w=majority")
    db = client.test
    db = client['datahillalpy']
    collection = db['lunarcrescentdatahilalpy']

    # read data from MongoDB collection
    data_mongo = []
    for doc in collection.find():
        data_mongo.append(doc)

# convert data to Pandas DataFrame
    df = pd.DataFrame(data_mongo)
    
    df.to_csv( data_loc, index=False, encoding='utf-8-sig')