import pandas as pd


def test_missing_values(df, column:str, expectation:float):
    null_ratio=df[column].isnull().mean()
    assert null_ratio<= expectation, f"'{column}' missing ratio too high: {null_ratio:.2%}"
    print('Passed')


def test_adults_range(df, expectation:float):
    valid_range = df['Adults'].between(1, 25)
    ratio_invalid = 1-valid_range.mean()

    assert ratio_invalid<=expectation, f"Too many invalid 'Adults' values. Invalid ratio: {ratio_invalid:.2%}"
    print('Passed')

def test_room_type(df, expectation:float):
    ratio_invalid=1-len(df[df.ReservedRoomType==df.AssignedRoomType])/len(df)

    assert ratio_invalid<=expectation, f"Too many ReservedRoomType vs AssignedRoomType mismatches. Invalid ratio: {ratio_invalid:.2%}"
    print('Passed')



df=pd.read_csv(r"data\hotels.csv",index_col=0)
test_missing_values(df,'Country',0.05)
test_adults_range(df,0.05)
test_room_type(df,0.10)