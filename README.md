# Tests
-Missing values checked:
    IsCanceled - planned to be the target variable
    LeadTime - key predictor
    ADR - important financial data, key for predicition or a potential target variable of its own
-Min/max range check:
    Adults - while some large groups are possible, a regular high values likely indicate data issues
-Room type match check:
    Regular mismatches between the reserved and assigned room types means either a significan business issue, or a data quality problem
-Valid category check:
    Deposit type - a potentially important predictor that has a well defined value range, unexpected values are a cause for concern
-Outliers:
    ADR - important financail indicater/predictor checked for outliers based on interquartile range