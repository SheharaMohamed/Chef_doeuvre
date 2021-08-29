import pandas as pd

def calc_percentage(dataframe, cols):

    for col in cols:
        lst = [dataframe[dataframe.année == dataframe['année'].min()][col].iloc[0]]
        lst.extend(dataframe[col][:-1].tolist())
        dataframe['temp'] = lst
        dataframe['perc_'+col.split('_')[1]] = (dataframe[col]*100/dataframe['temp'])-100
        dataframe.drop(columns = ['temp'], inplace = True)
    dataframe.drop(columns = cols, inplace = True)
    return(dataframe)

def backup(df,filename):
    import datetime;
    df = pd.DataFrame(df)
    ts = datetime.datetime.now()
    df.to_csv("{}.csv".format(filename))


