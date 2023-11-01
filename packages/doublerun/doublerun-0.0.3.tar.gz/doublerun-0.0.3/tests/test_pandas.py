from doublerun.pandas import (
    comparison_count,
    comparison_schema,
    comparison_columns,
    comparison_records,
    global_comparison
)

import pandas as pd

def test_comparison_count():
    df1 = pd.DataFrame({
        'Column1' : [1, 2, 3],
        'Column2' : ['A', 'B', 'C']
    })

    df2 = pd.DataFrame({
        'Column1' : [1, 2, 3, 4],
        'Column2' : ['E', 'B', 'C', 'F']
    })

    df3 = df2.copy()

    df1_count, df2_count = comparison_count(df1, df2)

    assert df1_count==3
    assert df2_count==4
    
    df2_count, df3_count = comparison_count(df2, df3)

    assert df2_count==4
    assert df3_count==4

def test_comparison_schema():

    df1 = pd.DataFrame({
        'Column1' : [1, 2, 3],
        'Column2' : ['A', 'B', 'C']
    })

    df2 = pd.DataFrame({
        'Column1' : [1, 2, 3, 4],
        'Column3' : ['E', 'B', 'C', 'F']
    })

    df3 = df2.copy()

    missing_columns_in_1, missing_columns_in_2 = comparison_schema(df1, df2)

    assert missing_columns_in_1==['Column3']
    assert missing_columns_in_2==['Column2']

    missing_columns_in_2, missing_columns_in_3 = comparison_schema(df2, df3)

    assert missing_columns_in_2==[]
    assert missing_columns_in_3==[]

def test_comparison_columns():

    df1 = pd.DataFrame({
        'Column1' : [1, 2, 3],
        'Column2' : ['A', 'B', 'C']
    })

    df2 = pd.DataFrame({
        'Column1' : [1, 2, 3, 4],
        'Column3' : ['E', 'B', 'C', 'F']
    })

    df3 = df2.copy()

    common_columns = comparison_columns(df1, df2)

    assert common_columns==['Column1']

    common_columns = comparison_columns(df2, df3)

    assert common_columns==['Column1', "Column3"]


def test_comparison_records():

    df1 = pd.DataFrame({
        'Column1' : [1, 2, 3, 4],
        'Column2' : ['A', 'B', 'C', 'D']
    })

    df2 = pd.DataFrame({
        'Column1' : [1, 2, 3, 4],
        'Column2' : ['E', 'B', 'C', 'F']
    })

    expected_left_diff  = df1.iloc[[0, 3]].reset_index(drop=True)
    expected_right_diff = df2.iloc[[0, 3]].reset_index(drop=True)
    expected_common     = df1.iloc[[1, 2]].reset_index(drop=True)

    common, left_diff, right_diff = comparison_records(df1, df2)

    pd.testing.assert_frame_equal(left_diff, expected_left_diff)
    pd.testing.assert_frame_equal(right_diff, expected_right_diff)
    pd.testing.assert_frame_equal(common, expected_common)

def test_global_comparison():

    df1 = pd.DataFrame({
        'Column1' : [1, 2, 3, 4],
        'Column2' : ['A', 'B', 'C', 'D']
    })

    df2 = pd.DataFrame({
        'Column1' : [1, 2, 3, 4],
        'Column2' : ['E', 'B', 'C', 'F']
    })

    expected_left_diff  = df1.iloc[[0, 3]].reset_index(drop=True)
    expected_right_diff = df2.iloc[[0, 3]].reset_index(drop=True)
    expected_common     = df1.iloc[[1, 2]].reset_index(drop=True)

    common, left_diff, right_diff = global_comparison(df1, df2)

    pd.testing.assert_frame_equal(left_diff, expected_left_diff)
    pd.testing.assert_frame_equal(right_diff, expected_right_diff)
    pd.testing.assert_frame_equal(common, expected_common)

