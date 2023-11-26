import psycopg2
import random
# Database connection parameters
from config import Config
db_params = {
    "host": Config.HOST,
    "database": Config.DATABASE,
    "user": Config.USER,
    "password": Config.PASSWORD
}

# Establish a connection to the PostgreSQL server
connection = psycopg2.connect(**db_params)

# Create a cursor object to interact with the database
cursor = connection.cursor()

def insert_dummy_data():
    try:
        # SQL queries to insert dummy data
        queries = []

        # Insert data into Account table
        for i in range(10, 21):
            account_type = random.choice(['Seller', 'Buyer', 'CarChecker', 'Mechanic'])
            queries.append(f"INSERT INTO Account (Username, Password, Email, Type) VALUES ('user{i}', 'pass{i}', 'user{i}@example.com', '{account_type}');")

        # Insert data into Seller table
        for i in range(1, 11):
            total_cars_sold = random.randint(1, 50)
            queries.append(f"INSERT INTO Seller (SellerID, Total_Cars_Sold) VALUES ({i}, {total_cars_sold});")

        # Insert data into Buyer table
        for i in range(1, 11):
            total_purchases = random.randint(1, 20)
            queries.append(f"INSERT INTO Buyer (BuyerID, Total_Purchases) VALUES ({i}, {total_purchases});")

        # Insert data into CarChecker table
        specializations = ['SUV', 'Sedan', 'Coupe', 'Convertible', 'Hatchback']
        for i in range(1, 11):
            specialization = random.choice(specializations)
            queries.append(f"INSERT INTO CarChecker (CheckerID, Specialization) VALUES ({i}, '{specialization}');")

        # Insert data into Mechanic table
        expertises = ['Engine Repair', 'Transmission', 'Brakes', 'Electrical', 'Bodywork']
        for i in range(1, 11):
            expertise = random.choice(expertises)
            queries.append(f"INSERT INTO Mechanic (MechanicID, Expertise) VALUES ({i}, '{expertise}');")

        # Insert data into CarUnchecked table
        for i in range(1, 11):
            year = random.randint(2010, 2023)
            seller_aid = random.randint(1, 10)
            status = random.choice(['Pending', 'Checked'])
            uncheck = 'TRUE' if status == 'Pending' else 'FALSE'
            queries.append(f"INSERT INTO CarUnchecked (Description, Model, Year, Status, Seller_AID, Uncheck) VALUES ('Model {i}', 'Model {i}', {year}, '{status}', {seller_aid}, {uncheck});")

        # Insert data into GreatCar and BrokenCar tables
        for i in range(1, 11):
            checker_id = random.randint(1, 10)
            if i % 2 == 0:
                queries.append(f"INSERT INTO GreatCar (UCID, CheckerID) VALUES ({i}, {checker_id});")
            else:
                queries.append(f"INSERT INTO BrokenCar (UCID, CheckerID) VALUES ({i}, {checker_id});")

        # Insert data into CarParts table
        part_names = ['Engine', 'Transmission', 'Brakes', 'Wheels', 'Exhaust']
        for i in range(1, 11):
            cid = random.randint(1, 10)
            mechanic_id = random.randint(1, 10)
            part_name = random.choice(part_names)
            queries.append(f"INSERT INTO CarParts (CID, MechanicID, PartName) VALUES ({cid}, {mechanic_id}, '{part_name}');")

        # Insert data into Transaction table
        for i in range(1, 11):
            buyer_id = random.randint(1, 10)
            seller_id = random.randint(1, 10)
            gcid = random.randint(1, 10)
            queries.append(f"INSERT INTO Transaction (BuyerID, SellerID, GCID) VALUES ({buyer_id}, {seller_id}, {gcid});")

        # Execute each query
        for query in queries:
            cursor.execute(query)

        # Commit the changes
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error inserting dummy data:", error)


    finally:
        # Close the cursor and the database connection
        if connection:
            cursor.close()
            connection.close()

insert_dummy_data()
