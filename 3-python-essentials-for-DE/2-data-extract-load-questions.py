# Extract: Process to pull data from Source system
# Load: Process to write data to a destination system

# Common upstream & downstream systems
# OLTP Databases: Postgres, MySQL, sqlite3, etc
# OLAP Databases: Snowflake, BigQuery, Clickhouse, DuckDB, etc
# Cloud data storage: AWS S3, GCP Cloud Store, Minio, etc
# Queue systems: Kafka, Redpanda, etc
# API
# Local disk: csv, excel, json, xml files
# SFTP\FTP server

# Databases: When reading or writing to a database we use a database driver. Database drivers are libraries that we can use to read or write to a database.
# Question: How do you read data from a sqlite3 database and write to a DuckDB database?
# Hint: Look at importing the database libraries for sqlite3 and duckdb and create connections to talk to the respective databases
import sqlite3 
sqlite_conn = sqlite3.connect("tpch.db")

# Fetch data from the SQLite Customer table
customers = sqlite_conn.execute("select * from customer").fetchall()
import duckdb
duckdb_conn = duckdb.connect("duckdb.db") # Duckdb connection string

# Insert data into the DuckDB Customer table
insert_query = f""" 
insert into customer (customer_id, zipcode, city, state_code, datetime_created, datetime_updated) 
values (?, ?, ?, ?, ?,?)"""
duckdb_conn.executemany(insert_query, customers)# insert into query

# Hint: Look for Commit and close the connections
# Commit tells the DB connection to send the data to the database and commit it, if you don't commit the data will not be inserted
duckdb_conn.commit()
# We should close the connection, as DB connections are expensive
sqlite3.close()
duckdb_conn.close()

# Cloud storage
# Question: How do you read data from the S3 location given below and write the data to a DuckDB database?
# Data source: https://docs.opendata.aws/noaa-ghcn-pds/readme.html station data at path "csv.gz/by_station/ASN00002022.csv.gz"
# Hint: Use boto3 client with UNSIGNED config to access the S3 bucket
# Hint: The data will be zipped you have to unzip it and decode it to utf-8
import csv
import gzip
from io import StringIO

import boto3 
import duckdb
from botocore import UNSIGNED
from botocore.client import Config

# AWS S3 bucket and file details
bucket_name = "noaa-ghcn-pds"
file_key = "csv.gz/by_station/ASN00002022.csv.gz"
# Create a boto3 client with anonymous access
s3_client = boto3.client("s3", config= Config(signature_version = UNSIGNED))

# Download the CSV file from S3
response = s3_client.get_object(Bucket=bucket_name, Key = file_key)
response["Body"].read()

# Decompress the gzip data
csv_data = gzip.decompress(compress_data).decode(uft-8)

# Read the CSV file using csv.reader
csv_reader= csv.reader(StringIO(csv_data))
data = list(csv_reader)

# Connect to the DuckDB database (assume WeatherData table exists)
duckdb_conn = duckdb.connect("duckdb.db")

# Insert data into the DuckDB WeatherData table
insert_query = """
insert into WeatherData (id, date, element, value, m_flag, q_flag, s_flag, obs_time)
value(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
duckdb_conn.executemange(insert_query, data[:1000000]
#commit and close connection
duckdb_conn.commit()
duckdb_conn.close()


# API
# Question: How do you read data from the CoinCap API given below and write the data to a DuckDB database?
# URL: "https://api.coincap.io/v2/exchanges"
# Hint: use requests library
import duckdb
import requests
# Define the API endpoint
url = "https://api.coincap.io/v2/exchanges"

# Fetch data from the CoinCap API
response = requests.get(url)
data = response.json()["data"]

# Connect to the DuckDB database
duckdb_conn = duckdb.connect("duckdb.db")

# Insert data into the DuckDB Exchanges table
insert_query = """
INSERT INTO Exchanges (id, name, rank, percentTotalVolume, volumeUsd, tradingPairs, socket, exchangeUrl, updated)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Prepare data for insertion
# Hint: Ensure that the data types of the data to be inserted is compatible with DuckDBs data column types in ./setup_db.py
insert_data = [
    (
        exchange["exchangeId"],
        exchange["name"],
        int(exchange["rank"]),
        (
            float(exchange["percentTotalVolume"])
            if exchange["percentTotalVolume"]
            else None
        ),
        float(exchange["volumeUsd"]) if exchange["volumeUsd"] else None,
        exchange["tradingPairs"],
        exchange["socket"],
        exchange["exchangeUrl"],
        int(exchange["updated"]),
    )
    for exchange in data
]
duckdb_conn.executemany(insert_query, insert_data)

# Local disk
# Question: How do you read a CSV file from local disk and write it to a database?
# Look up open function with csvreader for python

# Web scraping
# Questions: Use beatiful soup to scrape the below website and print all the links in that website
# URL of the website to scrape
url = 'https://example.com'


# SQLite3
# 	•	What it is: A lightweight, file-based database that doesn’t require a server.
# 	•	Best for:
# 	•	Small-scale applications.
# 	•	Prototyping and testing.
# 	•	Single-user or embedded applications.
# 	•	Strengths:
# 	•	Requires no setup (zero-configuration).
# 	•	Portable as it’s a single-file database.
# 	•	Excellent for lightweight data storage.
# 	•	Weaknesses:
# 	•	Limited scalability.
# 	•	Lacks advanced features like full-text search, stored procedures, or extensive concurrency.

# Using SQLite3 in Python:
import sqlite3 
# Connect to the database (or create one if it doesn't exist)
conn = sqlite3.connect('example.db')
# Create a cursor object
cursor = conn.cursor()

# Execute SQL commands
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES ('Alice')")

# Commit and close
conn.commit()
conn.close()


# PostgreSQL
# 	•	What it is: An advanced, open-source, relational database management system (RDBMS).
# 	•	Best for:
# 	•	Large-scale applications.
# 	•	Complex queries and operations.
# 	•	Applications requiring high reliability and data integrity.
# 	•	Strengths:
# 	•	Support for advanced features like JSON/JSONB, full-text search, and window functions.
# 	•	Extensible with plugins and custom functions.
# 	•	ACID compliance ensures high reliability.
# 	•	Weaknesses:
# 	•	Heavier setup and maintenance compared to SQLite.
# 	•	May be overkill for small applications.

# Using PostgreSQL in Python (with psycopg2):
import psycopg2

# Connect to the database
conn = psycopg2.connect(
    dbname='your_database',
    user='your_user',
    password='your_password',
    host='localhost',
    port='5432'
)

# Create a cursor object
cursor = conn.cursor()

# Execute SQL commands
cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES ('Alice')")

# Commit and close
conn.commit()
conn.close()

# MySQL
# 	•	What it is: Another popular open-source RDBMS.
# 	•	Best for:
# 	•	Web applications (e.g., LAMP stack).
# 	•	Medium to large-scale applications.
# 	•	Applications requiring high-speed performance for reads.
# 	•	Strengths:
# 	•	High performance for read-heavy workloads.
# 	•	Wide adoption and community support.
# 	•	Offers replication for scaling reads.
# 	•	Weaknesses:
# 	•	Historically less advanced than PostgreSQL for complex operations (although this has improved).
# 	•	Some licensing constraints for enterprise use (MySQL is now owned by Oracle).

# Using MySQL in Python (with mysql-connector-python):
import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host='localhost',
    user='your_user',
    password='your_password',
    database='your_database'
)

# Create a cursor object
cursor = conn.cursor()

# Execute SQL commands
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
cursor.execute("INSERT INTO users (name) VALUES ('Alice')")

# Commit and close
conn.commit()
conn.close()
