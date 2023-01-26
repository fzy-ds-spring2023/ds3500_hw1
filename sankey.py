
"""
sankey.py: A reusable library for sankey visualizations
"""
import pandas as pd
import plotly.graph_objects as go


def _group_data(df, src, targ, vals=None):
    # group by for each column pair and rename dataframe columns
    if vals:    
        return df.groupby([src, targ])[vals].sum().reset_index().rename(columns = {src:'source', targ:'target'})
    else:
        # rename aggregate column to vals=None to remove if statement for vals in make_sankey
        return df.groupby([src,targ]).size().reset_index().rename(columns = {src:'source', targ:'target', 0: vals})
    

def _code_mapping(df):
    # Get distinct labels
    labels = list(set(list(df["source"]) + list(df["target"])))

    # Get integer codes
    codes = list(range(len(labels)))

    # Create label to code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute names for codes in dataframe
    df = df.replace({"source": lc_map, "target": lc_map})

    return df, labels

def clean_records(df):
    # remove undefined/0 records from dataframe
    df.fillna(0, inplace=True)
    return df.loc[(df != 0).all(axis=1)].reset_index(drop=True)

def make_sankey(input_df, cols, vals=None, **kwargs):
    """ Create a sankey diagram linking src values to
    target values with thickness vals """
    assert len(cols) >= 2, "needs at least two columns" # require column list of at least 2 columns
    
    # initialize dataframe to concatenate
    df = pd.DataFrame()
    
    # iterate through each "pair" of columns
    for i in range(len(cols)-1):
        src = cols[i]
        targ = cols[i+1]
        _df = _group_data(input_df, src, targ, vals)
        df = pd.concat([df,_df], axis=0)
    
    # get sankey values
    df, labels = _code_mapping(df)
    
    # kwargs for better looking sankey diagrams, defaults=20
    df = df.loc[df[vals] >= kwargs.get('min_val', 20)]
    pad = kwargs.get('pad', 20)
    
    # build Sankey requisites
    link = {'source':df['source'], 'target':df['target'], 'value':df[vals]}
    node = {'label': labels, 'pad': pad}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    
    # write out plots to png with columns
    file = "_".join(cols)
    fig.write_image(f"plots/artist({file}).png")
    fig.show()

