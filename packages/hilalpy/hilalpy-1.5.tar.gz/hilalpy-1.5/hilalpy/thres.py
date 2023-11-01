def thres (figure,csv_stats,csv_maxmin,x):
    
    import os,glob, pandas as pd
    import numpy as np  
    import pandas as pd  
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numexpr as ne
    from pymongo import MongoClient


    #convert all varible to positive.
    #url = 'https://raw.githubusercontent.com/msyazwanfaid/hilalpy/main/Final.csv'
    #df = pd.read_csv(url, index_col=0)
    
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

    #Only take Visible Data
    df = df[df['V'] =='V']

    #Only Take Evening Observation
    df = df[df['O'] =='E']
    
    #Only Take Positive Data
    df = df[df[x] >=0]
    df_box_plot=df
    df_extract=df

    ##Generate the Boxplot
    a =sns.boxplot( y=df_box_plot["M"], x=df_box_plot[x],showfliers=False )
    plt.show()
    fig = a.get_figure()
    fig.savefig(figure)

    #Generate Statistics
    dft = df_box_plot[["M",x]] 
    df_by_m = dft.groupby('M')
    df_by_m.describe().to_csv(csv_stats)
    
    
    #find Naked Eye Minimum
    dfne = df_extract[df_extract['M'] =='NE']
    dfne = dfne[dfne[x] == min(dfne[x])]

    #Find Optical Aided Minumum
    dfoa = df_extract[df_extract['M'] =='OA']
    dfoa = dfoa[dfoa[x] == min(dfoa[x])]

    #Combine Naked Eye & Optical Aided
    dfc=pd.concat([dfne, dfoa], axis=0)

    #Drop Unnesscary Column
    dfc=dfc.drop(['Moonset', 'V', 'Sunset','TZ','O',"NE",'B','T','CCD'], axis = 1)

    #Output Min Value
    dfc.to_csv( csv_maxmin, index=False, encoding='utf-8-sig')
    

