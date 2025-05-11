# Data
Hotel booking demand dataset complied by Antonio et al. in 2018 (https://doi.org/10.1016/j.dib.2018.11.126) containing booking data from two Portuguese hotels over three years. The dataset contains 32 variables describing nearly 120 thousand bookings in total. A shortened and cleaned version can be found on Kaggle (https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand), but the complete original dataset was used in this exercise.

# Tests
All expected ratios are determined based on the first year of data. An entire year of data is used for setting expectations in order to capture all patterns likely to be seen in such a dataset, such as higher activity during summer/holidays or potentially more last-minute/flexible reservations during spring/early fall. A 5% margin of error is added, which is generally considered standard, and recommended by existing frameworks such as great expectations.
-Missing values checked:
    IsCanceled - planned to be the target variable, only accepted if there are no missing values
    LeadTime - key predictor
    ADR - important financial data, key for predicition or a potential target variable of its own
-Room type match check:
    Regular mismatches between the reserved and assigned room types means either a significan business issue, or a data quality problem
-Valid category check:
    Deposit type - a potentially important predictor that has a well defined value range, unexpected values are a cause for concern. The addition of any new categories would require manual update.
-Outliers:
    ADR - important financail indicator/predictor
    Adults - while some large groups are possible, a regular high values likely indicate data issues
