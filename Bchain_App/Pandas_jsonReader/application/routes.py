import Seedphrase_Generator as sp
import Username_Generator as ug
import pandas as pd
import random
from os import getenv

#df = pd.DataFrame(columns= ['username','password','mnemonic'])

def json_parser():
    df = pd.DataFrame(columns= ['username','password','mnemonic'])
    df_words = pd.read_json(sp.word_positioner(),orient='columns').sort_values(by='sp_order')
    df_usnpwd = pd.read_json(ug.usn_pwd())
    try:
        user_name = df_usnpwd.username[0] + str(random.randint(1000000000, 9999999999))
    except:
        user_name = str(random.randint(100000000000000, 999999999999999))
    print(len(user_name))
    if (len(df.loc[df.username == user_name])) == 0:
        if (len(user_name) <= 40):
    
            seedphrase = '' 
            for w in df_words.sp_words:
                seedphrase = seedphrase + w + '_'
            df_usnpwd['mnemonic'] = seedphrase
            df = df.append(df_usnpwd,ignore_index=True)
            return df.to_json()
        else:
            return 'Aww shucks! That username was too long. Try another one with fewer characters'
    else:
        return 'Aww shucks! That username is taken. Please try another one!'