import WordList_Reader as words
import WordList_Parser as positions
import pandas as pd

def word_positioner():
    sp = words.mnemonic_generator()
    indeces = positions.random_sequence()
    df1 = pd.read_json(words.mnemonic_generator(),orient='columns')
    df2 = pd.read_json(positions.random_sequence(),orient='columns').sort_index()
    df = pd.merge(df1,df2,how='right',left_index=True, right_index=True).sort_values(by='sp_order')
    return df.to_json()

