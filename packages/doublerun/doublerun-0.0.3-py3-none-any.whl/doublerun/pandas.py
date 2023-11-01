from typing import Tuple
import pandas as pd
from typing import List

def comparison_count(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Compare the number of rows between two DataFrames and prints the result.
    
    Args:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.

    Returns:
        None
    """

    print("COMPARAISON DU NOMBRE DE LIGNES".center(80, "*"))

    df1_count = df1.shape[0]
    df2_count = df2.shape[0]

    if df1_count!=df2_count:
        print(
            f"""
    Le nombre de lignes des deux DataFrames ne sont pas égaux :
        - Pour le DataFrame 1 on a {df1_count} lignes.
        - Pour le DataFrame 2 on a {df2_count} lignes.
            """)
    else:
        print(
            f"""
    Le nombre de lignes des deux DataFrames sont égaux: {df1_count}.
            """)
    
    return df1_count, df2_count
        
def comparison_schema(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Compare the schemas of two DataFrames and prints the result.
    
    Args:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.
    
    Returns: 
        Tuple[List[str], List[str]]: The columns missing in each DataFrame.
    """

    print("COMPARAISON DU SCHEMA".center(80, "*"))
    
    missing_columns_in_1 = [i for i in df2.columns if i not in df1.columns]
    missing_columns_in_2 = [i for i in df1.columns if i not in df2.columns]

    if (df1.columns!=df2.columns).any():
        print(
            f"""
    Les schémas ne sont pas équivalents.
    Dans le DataFrame 1 il y a ces colonnes manquantes par rapport au DataFrame 2:
        {missing_columns_in_1}
    
    Dans le DataFrame 2 il y a ces colonnes manquantes par rapport au DataFrame 1:
        {missing_columns_in_2}
            
            """)
    else:
        print("Les colonnes des deux DataFrames sont identiques.")

    return missing_columns_in_1, missing_columns_in_2

def comparison_columns(df1: pd.DataFrame, df2: pd.DataFrame) -> List[str]:
    """
    Compare the columns of two DataFrames and prints the result.
    
    Args:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.
    
    Returns:
        List[str]: The common columns between the two DataFrames.
    """

    print("COMPARAISON DES COLONNES".center(80, "*"))
    
    colonnes_communes = [i for i in df2.columns if i in df1.columns]

    col_diff = len(df1.columns) - len(df2.columns)

    if col_diff:

        larger_df = 1 if len(df1.columns) > len(df2.columns) else 2
        smaller_df = 2 if len(df1.columns) > len(df2.columns) else 1
        print(
        f"""
    Le nombre de colonnes du DataFrame {larger_df} ({eval(f"len(df{larger_df}.columns)")}) est supérieur à celui du DataFrame {smaller_df} ({eval(f"len(df{smaller_df}.columns)")}).
        Nombre de colonnes communes entre les deux DataFrames: {len(colonnes_communes)}
        Colonnes communes entre les deux DataFrames:
            {colonnes_communes}
        """)
    
    else:
        print(
            f"""
    Le nombre de colonnes est identiques entre les deux DataFrames.
        Nombre de colonnes communes entre les deux DataFrames: {len(colonnes_communes)}
        Colonnes communes entre les deux DataFrames: 
            {colonnes_communes}
        """)

    return colonnes_communes


def comparison_records(df1: pd.DataFrame, df2: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Compare the data between two DataFrames and prints the result.

    Args:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: 
            A tuple containing three DataFrames:
            1. Common rows between the two DataFrames.
            2. Rows present in df1 but not in df2.
            3. Rows present in df2 but not in df1.

    """

    print("COMPARAISON DES DONNÉES ENTRE LES DEUX DATAFRAMES".center(80, '*'))

    merged_df = df1.merge(df2, indicator=True, how='outer')

    left_diff  = merged_df[merged_df['_merge'] == 'left_only'].drop("_merge", axis=1).reset_index(drop = True)
    right_diff = merged_df[merged_df['_merge'] == 'right_only'].drop("_merge", axis=1).reset_index(drop = True)
    common     = merged_df[merged_df['_merge'] == 'both'].drop("_merge", axis=1).reset_index(drop = True)

    if left_diff.shape[0]!=0 or right_diff.shape[0]!=0:
        print(f"""
    Certaines lignes ne sont pas présentes dans les deux DataFrames:
            {left_diff.shape[0]} lignes sont uniquement dans le DataFrame 1.
            
            {right_diff.shape[0]} lignes sont uniquement dans le DataFrame 2.
            
            {common.shape[0]} lignes sont présentes dans les deux DataFrames.
        """)
        
    else:
        print("Toutes les lignes du DataFrame 1 sont présentes dans le DataFrame 2.")

    return common, left_diff, right_diff

def global_comparison(df1: pd.DataFrame, df2: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Perform a comprehensive comparison between two DataFrames and print the results.

    Args:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: 
            A tuple containing three DataFrames:
            1. Common rows between the two DataFrames.
            2. Rows present in df1 but not in df2.
            3. Rows present in df2 but not in df1.
    """
 
    comparison_count(df1, df2)
    comparison_schema(df1, df2)
    comparison_columns(df1, df2)
    common, left_diff, right_diff = comparison_records(df1, df2)

    return common, left_diff, right_diff