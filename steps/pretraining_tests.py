from zenml import step
import pandas as pd

class PretrainTests():
    def __init__(self, exp_df:pd.DataFrame, test_df:pd.DataFrame, margin:float=0.05):
        self.exp_df=exp_df
        self.test_df=test_df
        self.margin = margin

    def get_expectations(self):
        adr_missing = self.exp_df['ADR'].isnull().mean()
        lead_missing = self.exp_df['LeadTime'].isnull().mean()

        room_mismatch = 1 - len(self.exp_df[self.exp_df.ReservedRoomType == self.exp_df.AssignedRoomType]) / len(self.exp_df)

        adults_outlier = self.get_quartile_outlier(self.exp_df, 'Adults')
        adr_outlier = self.get_quartile_outlier(self.exp_df, 'ADR')

        return [
            min(1.0, adr_missing + self.margin),
            min(1.0, lead_missing + self.margin),
            min(1.0, room_mismatch + self.margin),
            min(1.0, adults_outlier + self.margin),
            min(1.0, adr_outlier + self.margin)]

    def get_quartile_outlier(self,df:pd.DataFrame,col:str):
        data=df[col]
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = data[(data < lower_bound) | (data > upper_bound)]
        return len(outliers) / len(data)

    def run_tests(self,expectations):
        return [
            self.test_missing_values(self.test_df,'IsCanceled',0.0),
            self.test_missing_values(self.test_df,'ADR',expectations[0]),
            self.test_missing_values(self.test_df,'LeadTime',expectations[1]),

            self.test_room_type(self.test_df,expectations[2]),
            self.test_deposit_type_valid_categories(self.test_df),
            self.test_quartile_outlier(self.test_df,'Adults',expectations[3]),
            self.test_quartile_outlier(self.test_df,'ADR',expectations[4])]


    def test_missing_values(self,df:pd.DataFrame, column:str, expectation:float):
        null_ratio=df[column].isnull().mean()
        if null_ratio<= expectation:
            print(f'Passed missing values test for column {column}')
            return True
        else:
            print(f"'{column}' missing ratio too high: {null_ratio:.2%}, expected: {expectation:.2%}")
            return False


    def test_range(self,df:pd.DataFrame, col:str, min:int, max:int, expectation:float):
        valid_range = df[col].between(min, max)
        ratio_invalid = 1-valid_range.mean()

        if ratio_invalid<=expectation:
            print(f'Passed range test for column {col}')
            return True
        else:
            print(f"Too many invalid {col} values. Invalid ratio: {ratio_invalid:.2%}, expected: {expectation:.2%}")
            return False
        

    def test_room_type(self,df:pd.DataFrame, expectation:float):
        ratio_invalid=1-len(df[df.ReservedRoomType==df.AssignedRoomType])/len(df)
        if ratio_invalid<=expectation:
            print(f'Passed room type test')
            return True
        else:
            print(f"Too many ReservedRoomType vs AssignedRoomType mismatches. Invalid ratio: {ratio_invalid:.2%}, expected: {expectation:.2%}")
            return False
        

    def test_deposit_type_valid_categories(self,df:pd.DataFrame):
        expected_deposits = {"No Deposit", "Non Refund", "Refundable"}
        actual = set(df['DepositType'].dropna().unique())
        diff = actual - expected_deposits
        if diff:
            print(f"Unexpected DepositType values: {diff}")
            return False
        else:
            print(f'Passed deposit type test')
            return True


    def test_quartile_outlier(self, df:pd.DataFrame,col:str, expectation:float):
        outlier_ratio = self.get_quartile_outlier(df,col)
        if outlier_ratio < expectation:
            print(f'Passed outlier test for column {col}')
            return True
        else:
            print(f'{col} has too many outliers ({outlier_ratio:.2%}), expected: {expectation:.2%}')
            return False
        

@step
def run_data_quality_tests(train_df: pd.DataFrame) -> bool:
    exp_df = pd.read_csv("data/expectations.csv", index_col=0)
    
    test = PretrainTests(exp_df, train_df, margin= 0.08)
    expectations = test.get_expectations()
    results = test.run_tests(expectations)
    return all(results)