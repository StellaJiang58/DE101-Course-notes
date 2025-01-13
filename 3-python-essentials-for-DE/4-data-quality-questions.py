# Key Goals of the Code
# 	1.	Ensure Customer_ID Column is Complete:
# 	•	No null (missing) values in the Customer_ID column.
# 	2.	Ensure Customer_ID Column is Unique:
# 	•	Each value in the Customer_ID column must be unique (no duplicates).
# 	3.	Validate and Assert Results:
# 	•	Run these checks and ensure that all validations pass, with no failures.

# Polars is a high-performance DataFrame library similar to Pandas but faster and optimized for large datasets.
import polars as pl
from cuallee import Check, CheckLevel
# The Cuallee library is a Python library designed for data quality validation. It is particularly useful 
# for ensuring that data meets certain standards or rules before being used in downstream processes such as analytics, machine learning, or reporting.

# Read CSV file into Polars DataFrame
df = pl.read_csv("./data/sample_data.csv")

# Question: Check for Nulls on column Id and that Customer_ID column is unique
check = Check(CheckLevel.ERROR, "Completeness")

# CheckLevel.ERROR:Sets the severity level of the check (e.g., WARNING, ERROR).
# "Completeness": A label or name for this group of checks.


# check docs at https://canimus.github.io/cuallee/polars/ on how to define a check and run it.
# you will end up with a dataframe of results, check that the `status` column does not have any "FAIL" in it
validation_result_df = (check.is_complete("Customer_ID").is_unique("Customer_ID").validate(df))
# is_complete("Customer_ID"):	Checks that the Customer_ID column contains no null values.
# is_unique("Customer_ID"): Checks that the Customer_ID column has no duplicate values.
# validate(df): Runs the defined checks (is_complete and is_unique) on the Polars DataFrame (df).
# Output: validation_results_df is a Polars DataFrame containing the results of each check.

print(validation_result_df)
# check_name          column_name    status
# is_complete         Customer_ID    PASS
# is_unique           Customer_ID    PASS

result = validation_result_df['status'].to_list()
assert "FAIL" not in results == True
# Extract status Column:
# 	•	Converts the status column from the results DataFrame into a Python list.
# 	•	Example: results = ["PASS", "PASS"].
# Assert Validation:
# 	•	Checks that "FAIL" is not in the results list.
# 	•	If any check fails, the code raises an AssertionError.


import pandas as pd
from cuallee import Check, CheckLevel

# Create a sample DataFrame
df = pd.DataFrame({
    "Customer_ID": [1, 2, 3, None],
    "Sales": [100, 200, 300, 400]
})

# Define and execute checks
check = Check(CheckLevel.ERROR, "Data Validation")
validation_results = (
    check.is_complete("Customer_ID")
         .is_unique("Customer_ID")
         .validate(df)
)

# Print validation results
print(validation_results)

# output
check_name          column_name    status
is_complete         Customer_ID    FAIL
is_unique           Customer_ID    PASS
