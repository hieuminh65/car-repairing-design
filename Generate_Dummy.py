import psycopg2

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
        queries = [
            # Insert data into Employee table
            '''
            INSERT INTO Employee (EID, Name, Email, Phone, Position) VALUES
            (1, 'John Doe', 'john@example.com', '123-456-7890', 'CarChecker'),
            (2, 'Alice Smith', 'alice@example.com', '987-654-3210', 'Mechanic'),
            (3, 'Bob Johnson', 'bob@example.com', '456-789-0123', 'Mechanic'),
            (4, 'Ella Gray', 'ella@example.com', '345-678-9012', 'CarChecker'),
            (5, 'Mike Brown', 'mike@example.com', '234-567-8901', 'Mechanic');
            ''',

            # Insert data into CarChecker table
            '''
            INSERT INTO CarChecker (CheckerID, Specialization) VALUES
            (1, 'SUVs'),
            (4, 'Sedans');
            ''',

            # Insert data into Mechanic table
            '''
            INSERT INTO Mechanic (MechanicID, Expertise) VALUES
            (2, 'Engine Repairs'),
            (3, 'Brakes'),
            (5, 'Transmission');
            ''',

            # Insert data into Account table
            '''
            INSERT INTO Account (AID, Username, Password, Email, Type) VALUES
            (6, 'seller1', 'password1', 'seller1@example.com', 'Seller'),
            (7, 'seller2', 'password2', 'seller2@example.com', 'Seller'),
            (8, 'buyer1', 'password3', 'buyer1@example.com', 'Buyer'),
            (9, 'buyer2', 'password4', 'buyer2@example.com', 'Buyer'),
            (10, 'buyer3', 'password5', 'buyer3@example.com', 'Buyer');
            ''',

            # Insert data into Seller table
            '''
            INSERT INTO Seller (SellerID, Total_Cars_Sold) VALUES
            (6, 15),
            (7, 20);
            ''',

            # Insert data into Buyer table
            '''
            INSERT INTO Buyer (BuyerID, Total_Purchases) VALUES
            (8, 5),
            (9, 3),
            (10, 2);
            ''',

            # Insert data into Car table
            '''
            INSERT INTO Car (CID, Description, Model, Year, Status, Seller_AID, CheckerID) VALUES
            (1, 'A great family car', 'SUV Model X', 2020, 'Available', 6, 1),
            (2, 'Sporty and fast', 'Coupe Model Y', 2021, 'Available', 7, 4),
            (3, 'Comfort and luxury', 'Sedan Model Z', 2019, 'Sold', 6, 1),
            (4, 'Economical city car', 'Hatchback Model A', 2018, 'Available', 7, 4),
            (5, 'Off-road capability', '4x4 Model B', 2020, 'Sold', 6, 1);
            ''',

            # Insert data into CarParts table
            '''
            INSERT INTO CarParts (CID, PartName, Description) VALUES
            (1, 'Engine', 'V6 3.0L'),
            (1, 'Transmission', 'Automatic 6-speed'),
            (2, 'Engine', 'V4 2.0L Turbocharged'),
            (2, 'Wheels', '18-inch alloy wheels'),
            (3, 'Engine', 'V4 1.8L Hybrid');
            ''',

            # Insert data into Transaction table
            '''
            INSERT INTO Transaction (TransactionID, BuyerID, SellerID, CID, Amount, Date) VALUES
            (1, 8, 6, 3, 22000.50, '2023-01-15'),
            (2, 9, 7, 5, 26000.00, '2023-02-01'),
            (3, 10, 6, 1, 18000.75, '2023-03-20'),
            (4, 8, 7, 4, 15000.25, '2023-04-05'),
            (5, 9, 6, 2, 30000.00, '2023-05-12');
            '''
        ]

        # Execute each query to insert dummy data
        for query in queries:
            cursor.execute(query)

        # Commit the changes to the database
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error inserting dummy data:", error)

    finally:
        # Close the cursor and the database connection
        if connection:
            cursor.close()
            connection.close()

insert_dummy_data()
