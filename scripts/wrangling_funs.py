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

def read_and_clean_fines_data(path: str)->pd.DataFrame:
    """
    Reads in the scraped fines data, filters for positive price values only.
    """
    fines_df = (
        pd.read_csv(path, parse_dates=["date"])
        .pipe(filter_for_positives, "price")
        .pipe(strip_text_col, "type")
    )

    return fines_df

def pivot_fines_longer(df: pd.DataFrame)-> pd.DataFrame:
    """
    
    """

    long_fines_df = (
        df
        .set_index('id')
        .articleViolated.str.extractall(r'([Aa]rt *. *\d+)')
        .reset_index()
        .rename(columns={0:'article'})
        .assign(
            n_articles_violated = lambda x: x.groupby('id').match.transform('max').astype('Int64') + 1,
            article_number      = lambda x: x.article.str.extract(r'(\d+)').astype('float').astype('Int64'))
        .merge(df, how='left', left_on='id', right_on='id')
        .loc[:, ['id', 'name', 'price', 'authority', 'date', 'controller',
                'articleViolated',
                'article_number', 'n_articles_violated', 'type', 'summary']]
        .rename(columns={'price':'total_fine_euro', 'name': 'country'})
    )
    return long_fines_df
    
