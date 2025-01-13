print("################################################################################")
print("Use standard python libraries to do the transformations")
print("################################################################################")

# Question: How do you read data from a CSV file at ./data/sample_data.csv into a list of dictionaries?
import csv
data =[]
data_location = "./data/sample_data.csv"
with open(data_location,"r", newline = "") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append() 
        
# Question: How do you remove duplicate rows based on customer ID?
data_unique = []
customer_ids_seen = set()
for row in data:
    if row["Customer_ID""] not in customer_ids_seen:
        data_unique.append()
        customer_ids_seen.add(row["Customer_ID"])
    else:
        print(f'duplciate customer id {row["Customer_ID"]}')
    
# Question: How do you handle missing values by replacing them with 0?
for row in data_unique():
    if not row['Age']:
        print(f'Customer for {row["Customer_ID"]} does not have age value')
        row['Age'] = 0
    if not row['Purchase_Amount']:
        row['Purchase_Amount'] = 0.0
        
# Question: How do you remove outliers such as age > 100 or purchase amount > 1000?
data_cleaned = [row for row in data if int(row['Age']) <= 100 and float(row['Purchase_Amount']) <= 1000]

# Question: How do you convert the Gender column to a binary format (0 for Female, 1 for Male)?
for row in data_cleaned:
    if row['Gender'] == "Female":
        row['Gender'] = 0
    elif row['Gender'] == "Male":
        row['Gender'] = 1
        
# Question: How do you split the Customer_Name column into separate First_Name and Last_Name columns?
for row in data_cleaned:
    first_name, last_name = row['Customer_Name'].split(" ", 1)
    row['First_Name'] = first_name
    row['Last_Name'] = last_name
    del row['Customer_Name']

# Question: How do you calculate the total purchase amount by Gender?
total_purchase_by_gender = {}
for row in data_cleaned:
    total_purchase_by_gender[row['Gender'] += float(row['Purchase_Amount'])

# Question: How do you calculate the average purchase amount by Age group?
# assume age_groups is the grouping we want
# hint: Why do we convert to float?
age_groups = {"18-30": [], "31-40": [], "41-50": [], "51-60": [], "61-70": []}
for row in data_cleaned:
    age = int(row['Age'])
    if age <= 30:
        age_groups["18-30"].append(float(row["Purchase_Amount"]))
    elif age <= 40:
        age_groups["31-40"].append(float(row["Purchase_Amount"]))
    elif age <= 50:
        age_groups["41-50"].append(float(row["Purchase_Amount"]))
    elif age <= 60:
        age_groups["51-60"].append(float(row["Purchase_Amount"]))
    else:
        age_groups["61-70"].append(float(row["Purchase_Amount"])) 

# Question: How do you print the results for total purchase amount by Gender and average purchase amount by Age group?
total_purchase_amount_by_gender = {} # your results should be assigned to this variable
average_purchase_by_age_group = {group: sum(amounts)/len(amounts) for group, amount in age_groups.items} # your results should be assigned to this variable

print(f"Total purchase amount by Gender: {total_purchase_amount_by_gender}")
print(f"Average purchase amount by Age group: {average_purchase_by_age_group}")

print("################################################################################")
print("Use DuckDB to do the transformations")
print("################################################################################")

# Question: How do you connect to DuckDB and load data from a CSV file into a DuckDB table?
# Connect to DuckDB and load data
import duckdb
# Indicates that the database is created and stored in memory rather than on disk.
# read_only=False: Specifies that the connection allows write operations.
duckdb_conn= duckdb.connect(database = ":memory:", read_only = False)
duckdb_conn.execute(
    "CREATE TABLE data (Customer_ID INTEGER, Customer_Name VARCHAR, Age INTEGER, Gender VARCHAR, Purchase_Amount FLOAT, Purchase_Date DATE)"
)

# Read data from CSV file into DuckDB table
data_location = './data/sample_data.csv'
duckdb_conn.excute('copy data from data_location with (HEADER, FORMAT CSV)')
# HEADER: Indicates that the first row in the CSV file contains the column names (not actual data).
#FORMAT CSV: Specifies that the file format is CSV (Comma-Separated Values)

# Question: How do you remove duplicate rows based on customer ID in DuckDB?
duckdb_conn.excute('CREATE TABLE data_unique AS SELECT DISTINCT * FROM data')

# Question: How do you handle missing values by replacing them with 0 in DuckDB?
duckdb_conn.excute(
     "CREATE TABLE data_cleaned_missing AS SELECT \
             Customer_ID, Customer_Name, \
             COALESCE(Age, 0) AS Age, \
             Gender, \
             COALESCE(Purchase_Amount, 0.0) AS Purchase_Amount, \
             Purchase_Date \
             FROM data_unique"
)

# Question: How do you remove outliers (e.g., age > 100 or purchase amount > 1000) in DuckDB?
duckdb_conn.excute("CREATE TABLE data_cleaned_outlier AS SELECT * FROM data_cleaned_missing\
                   where age <= 100 and purchase_amount <= 1000")

# Question: How do you convert the Gender column to a binary format (0 for Female, 1 for Male) in DuckDB?
duckdb_conn.excute("CREATE TABLE data_cleaned_gender AS SELECT *, CASE WHEN Gender = 'Female' THEN 0 ELSE 1 END AS Gender_Binary \
             FROM data_cleaned_outliers")

# Question: How do you split the Customer_Name column into separate First_Name and Last_Name columns in DuckDB?
duckdb_conn.excute("CREATE TABLE data_cleaned AS SELECT \
             Customer_ID, \
             SPLIT_PART(Customer_Name, ' ', 1) AS First_Name, \
             SPLIT_PART(Customer_Name, ' ', 2) AS Last_Name, \
             Age, Gender_Binary, Purchase_Amount, Purchase_Date \
             FROM data_cleaned_gender")

# Question: How do you calculate the total purchase amount by Gender in DuckDB?
total_purchase_by_gender = con.execute("SELECT  Gender_Binary, SUM(Purchase_Amount) AS Total_Purchase_Amount \
                                        FROM data_cleaned_gender \
                                        GROUP BY Gender_Binary").fetchall()

# Question: How do you calculate the average purchase amount by Age group in DuckDB?
average_purchase_by_age_group = con.execute(
    "SELECT CASE WHEN Age BETWEEN 18 AND 30 THEN '18-30' \
                 WHEN Age BETWEEN 31 AND 40 THEN '31-40' \
                 WHEN Age BETWEEN 41 AND 50 THEN '41-50' \
                 WHEN Age BETWEEN 51 AND 60 THEN '51-60' \
                 ELSE '61-70' END AS Age_Group, \
                 AVG(Purchase_Amount) AS Average_Purchase_Amount \
                 FROM data_cleaned \
                 GROUP BY Age_Group"
).fetchall()

# Question: How do you print the results for total purchase amount by Gender and average purchase amount by Age group in DuckDB?
print("====================== Results ======================")
print("Total purchase amount by Gender:")
print("Average purchase amount by Age group:")
