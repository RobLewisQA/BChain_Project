import pandas as pd
import Password_Generator as pg
import random

def usn_pwd():
    user_name = input() + str(random.randint(1000000000, 9999999999))
    password = pd.read_json(pg.password_engine()).iloc[:,0][0]
    df = pd.DataFrame.from_dict({'username':user_name,'password': password},orient='index').T
    #print(password)
    #df1 = df.to_json()
    return df.to_json()