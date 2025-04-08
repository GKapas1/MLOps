import pandas as pd
import pytest


def test_missing_values(df:pd.DataFrame, column:str, expectation:float):
    null_ratio=df[column].isnull().mean()
    assert null_ratio<= expectation, f"'{column}' missing ratio too high: {null_ratio:.2%}"
    print('Passed')


def test_adults_range(df:pd.DataFrame, expectation:float):
    valid_range = df['Adults'].between(1, 25)
    ratio_invalid = 1-valid_range.mean()

    assert ratio_invalid<=expectation, f"Too many invalid 'Adults' values. Invalid ratio: {ratio_invalid:.2%}"
    print('Passed')

def test_room_type(df:pd.DataFrame, expectation:float):
    ratio_invalid=1-len(df[df.ReservedRoomType==df.AssignedRoomType])/len(df)
    assert ratio_invalid<=expectation, f"Too many ReservedRoomType vs AssignedRoomType mismatches. Invalid ratio: {ratio_invalid:.2%}"
    print('Passed')

def test_deposit_type_valid_categories(df:pd.DataFrame):
    expected_deposits = {"No Deposit", "Non Refund", "Refundable"}
    actual = set(df['DepositType'].dropna().unique())
    diff = actual - expected_deposits
    assert not diff, f"Unexpected DepositType values: {diff}"
    print('Passed')

def test_quartile_outlier(df:pd.DataFrame,col:str, expectation:float):
    data=df[col]
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = data[(data < lower_bound) | (data > upper_bound)]
    outlier_ratio = len(outliers) / len(data)

    assert outlier_ratio < expectation, (
        f"{col} has too many outliers ({outlier_ratio:.2%}). "
        f"Expected <5%. IQR bounds: [{lower_bound:.2f}, {upper_bound:.2f}]"
    )
    print('Passed')




df=pd.read_csv(r"data\hotels.csv",index_col=0)
test_missing_values(df,'Country',0.05)
test_adults_range(df,0.05)
test_room_type(df,0.10)
test_deposit_type_valid_categories(df)
test_quartile_outlier(df,'ADR',0.05)