from db_connection import fetch_data

# Test fetching data from the Patients table
data = fetch_data("SELECT * FROM Patients")

if data:
    print("Fetched data:")
    for row in data:
        print(row)
else:
    print("No data fetched.")