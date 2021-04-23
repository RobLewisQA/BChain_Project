import random
import pandas as pd

def password_engine():
    chars = ['a','b','c','d','e','f',
             'g','h','i','j','k','l',
             'm','n','o','p','q','r',
             's','t','u','v','w','x',
             'y','z','!','£','$','%',
             '^','&','%','*','(',')',
             '_','+','~','@','/','A',
             'B','C','D','E','F','G',
             'H','I','J','K','L','M',
             'N','O','P','Q','W','X',
             'Y','Z','0','1','2','3',
             '4','5','6','7','8','9',
             'a','b','c','d','e','f']
    password = ''
    while len(password) < random.randint(10,13):
        password = password + chars[random.randint(0,len(chars)-1)]
    df = pd.DataFrame.from_dict({'password': password},orient='index').T
    return df.to_json()