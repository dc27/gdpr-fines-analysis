import numpy as np
import pandas as pd

def filter_for_positives(df: pd.DataFrame, column:str)->pd.DataFrame:
    """
    Filters a column of interest in a pandas dataframe to contain only positive values.
    """

    # should bools be numbers? Let's say no
    if df[column].dtype == np.bool_:
        raise TypeError

    return df.loc[df[column] > 0, :].reset_index(drop=True)


def strip_text_col(df: pd.DataFrame, column:str)->pd.DataFrame:
    """
    Removes whitespace from a column of interest in a pandas dataframe
    """

    # only attempt text (object) values
    if df[column].dtype != np.object_:
        raise TypeError

    df[column] = df[column].str.strip()
    return df
