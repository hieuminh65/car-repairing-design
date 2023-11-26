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


# connect to database

def CreateTestTable():

    try:

        # Execute SQL query to create a new database
        create_new_table = f'''

        -- Create a new table for employees
        CREATE TABLE employees (
            employee_id SERIAL PRIMARY KEY,   -- Assuming an auto-incrementing primary key
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            position VARCHAR(50),
            date_joined DATE
        );

        -- Insert 5 dummy rows into the employees table
        INSERT INTO employees (first_name, last_name, position, date_joined)
        VALUES 
        ('John', 'Doe', 'Manager', '2021-01-10'),
        ('Jane', 'Smith', 'Developer', '2020-12-15'),
        ('Alice', 'Johnson', 'Designer', '2022-05-05'),
        ('Bob', 'Brown', 'Tester', '2021-06-20'),
        ('Charlie', 'Davis', 'Admin', '2019-11-03');

        '''
        cursor.execute(create_new_table)

        # Commit the transaction to create the new database
        connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error creating database:", error)

    finally:
        # Close the cursor and the database connection
        if connection:
            cursor.close()
            connection.close()


# get all rows from table 
def GetAllRowsFromTable(table_name):
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()

    # Print the rows
    print("employee_id | first_name | last_name | position  | date_joined")
    print("---------------------------------------------------------------")
    for row in rows:
        print(f"{row[0]:<12} | {row[1]:<10} | {row[2]:<9} | {row[3]:<9} | {row[4]}")

    # Close the cursor and connection
    cursor.close()
    connection.close()


def DropTable(table_name):
    cursor.execute(f"DROP TABLE {table_name};")

# first create a table
#CreateTestTable()


# get all rows from the table
DropTable('employees')
