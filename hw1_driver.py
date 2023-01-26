import pandas as pd
import sankey as sk
import itertools
from plotly.subplots import make_subplots

    
def main():
    # build dataframe with needed info from json file and clean for decades
    df_artist = pd.read_json("data/Artists.json")[['Nationality', 'Gender', 'BeginDate']]
    df_artist['BeginDate'] = df_artist['BeginDate'].map(lambda x: int(x - x%10))
    df_artist.rename({'BeginDate': 'Decade'}, axis=1, inplace=True)
    df_artist = df_artist.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    # clean undefined/0 records in dataframe
    df_artist = sk.clean_records(df_artist)
    
    # get every combination of 2-3 columns for df_artist
    for i in range(2,4):
        for subset in itertools.combinations(df_artist.columns, i):
            sk.make_sankey(df_artist, subset)
        
    
if __name__ == '__main__':
    main()