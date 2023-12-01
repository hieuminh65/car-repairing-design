import psycopg2
from config import Config

    
# Database connection parameters
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


def create_tables():
    try:
        # SQL queries to create tables based on the provided schema
        queries = [

            # Account table
            '''
            CREATE TABLE Account (
                AID SERIAL PRIMARY KEY,
                Username VARCHAR(50) NOT NULL,
                Password VARCHAR(100) NOT NULL,
                Email VARCHAR(100) NOT NULL,
                Type VARCHAR(50) NOT NULL
            );
            ''',

            # Admin table
            '''
            CREATE TABLE Admin (
                AdminID INT PRIMARY KEY REFERENCES Account(AID) ON DELETE CASCADE
            );
            ''',

            # Seller table
            '''
            CREATE TABLE Seller (
                SellerID INT PRIMARY KEY REFERENCES Account(AID) ON DELETE CASCADE,
                Total_Cars_Sold INT
            );
            ''',

            # Buyer table
            '''
            CREATE TABLE Buyer (
                BuyerID INT PRIMARY KEY REFERENCES Account(AID) ON DELETE CASCADE,
                Total_Purchases INT
            );
            ''',

            # CarChecker table
            '''
            CREATE TABLE CarChecker (
                CheckerID INT PRIMARY KEY REFERENCES Account(AID),
                Specialization VARCHAR(100)
            );
            ''',

            # Mechanic table
            '''
            CREATE TABLE Mechanic (
                MechanicID INT PRIMARY KEY REFERENCES Account(AID),
                Expertise VARCHAR(100)
            );
            ''',

            # CarUnchecked table
            '''
            CREATE TABLE CarUnchecked (
                UCID SERIAL PRIMARY KEY,
                Description VARCHAR(255) NOT NULL,
                Model VARCHAR(50) NOT NULL,
                Year INT NOT NULL,
                Status VARCHAR(50) NOT NULL,
                Seller_AID INT REFERENCES Seller(SellerID),
                Uncheck BOOLEAN DEFAULT TRUE
            );
            ''',

            # GreatCar table
            '''
            CREATE TABLE GreatCar (
                GCID SERIAL PRIMARY KEY,
                UCID INT REFERENCES CarUnchecked(UCID)
            );
            ''',

            # BrokenCar table
            '''
            CREATE TABLE BrokenCar (
                BCID SERIAL PRIMARY KEY,
                UCID INT REFERENCES CarUnchecked(UCID)
            );
            ''',

            # CarParts table
            '''
            CREATE TABLE CarParts (
                PartID SERIAL PRIMARY KEY,
                CID INT REFERENCES CarUnchecked(UCID) ON DELETE CASCADE,
                MechanicID INT REFERENCES Mechanic(MechanicID),
                PartName VARCHAR(100) NOT NULL
            );
            ''',

            # Transaction table
            '''
            CREATE TABLE Transaction (
                TransactionID SERIAL PRIMARY KEY,
                BuyerID INT REFERENCES Buyer(BuyerID),
                SellerID INT REFERENCES Seller(SellerID),
                GCID INT REFERENCES carunchecked(UCID)
            );
            '''
            # Trigger
            '''
            CREATE OR REPLACE FUNCTION grant_select_to_new_admin()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Grant SELECT privilege to the new admin user
                EXECUTE 'GRANT SELECT ON ALL TABLES IN SCHEMA public TO ' || NEW.AdminID || ';'
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            '''
            '''
            CREATE TRIGGER after_insert_admin
            AFTER INSERT ON Admin
            FOR EACH ROW
            EXECUTE FUNCTION grant_select_to_new_admin();
            '''
        ]

        # Execute each query
        for query in queries:
            cursor.execute(query)

        # Commit the changes
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error creating tables:", error)

    finally:
        # Close the cursor and the database connection
        if connection:
            cursor.close()
            connection.close()

create_tables()
