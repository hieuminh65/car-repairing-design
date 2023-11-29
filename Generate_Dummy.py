import psycopg2

# Database connection parameters
db_params = {
    "host": "localhost",
    "database": "final_project",
    "user": "postgres",
    "password": "Toanposgre"
}

# Establish a connection to the PostgreSQL server
connection = psycopg2.connect(**db_params)

# Create a cursor object to interact with the database
cursor = connection.cursor()

def insert_dummy_data():
    try:
        # SQL queries to insert dummy data
        queries = [
            # Insert into accounts
            '''
            INSERT INTO account (username, password, email, type) VALUES 
            ('toan mechanic', 'Abcd12345@', 'toanmechanic@gmail.com', 'Mechanic'),
            ('toan carchecker', 'Abcd12345@', 'toancarchecker@gmail.com', 'CarChecker'),
            ('toan buyer', 'Abcd12345@', 'toanbuyer@gmail.com', 'Buyer'),
            ('toan seller', 'Abcd12345@', 'toanseller@gmail.com', 'Seller');
            ''',

            # Insert data into CarChecker table
            '''
            INSERT INTO CarChecker (CheckerID, Specialization) VALUES
            (2, 'I am a great car checker');
            ''',

            # Insert data into Mechanic table
            '''
            INSERT INTO Mechanic (mechanicid, Expertise) VALUES
            (1, 'I am a great car mechanic');
            ''',

            # Seller
            '''
            INSERT INTO seller (sellerid, total_cars_sold) VALUES 
            (4, 0);
            '''
            
            # Buyer
            '''
            INSERT INTO buyer (buyerid, total_purchases) VALUES 
            (3, 0);
            '''
                
            # Insert data into Carunchecked
            '''
            INSERT INTO Carunchecked (ucid, description, model, year, status, seller_aid, uncheck) VALUES
            (1, 'A new car', 'SUV Model X', 2020, 'New', 4, FALSE),
            (2, 'An old, 5000 miles car', 'Coupe Model Y', 2021, 'Used', 4, FALSE),
            (3, 'A broken car', 'Sedan Model Z', 2019, 'Damaged', 4, FALSE),
            (4, 'A well-maintained family car', 'Minivan Model A', 2018, 'Used', 4, FALSE),
            (5, 'A sports car with low mileage', 'Sports Model B', 2022, 'New', 4, TRUE),
            (6, 'A vintage car, needs some work', 'Classic Model C', 1965, 'Damaged', 4, FALSE),
            (7, 'An electric car, barely used', 'Electric Model D', 2023, 'New', 4, FALSE),
            (8, 'A compact city car', 'Hatchback Model E', 2021, 'Used', 4, TRUE),
            (9, 'A luxury car, recently serviced', 'Luxury Model F', 2020, 'Used', 4, TRUE),
            (10, 'An off-road vehicle, minor exterior damage', '4x4 Model G', 2019, 'Damaged', 4, TRUE);
            ''',

            # great car table
            '''
            INSERT INTO greatcar (ucid) VALUES
            (1),
            (7);
            ''',

            # broken car
            '''
            INSERT INTO brokencar (ucid) VALUES
            (2),
            (4);
            ''',

            # Insert data into CarParts table
            '''
            INSERT INTO CarParts (cid, mechanicid, partname) VALUES
            (3, 1, 'To be updated...'),
            (6, 1, 'To be updated...');
            ''',
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
