import streamlit as st
import psycopg2

# login function
from login import login_main
from SellerGUI import SellerMain
from BuyerGUI import BuyerMain
from CarCheckerGUI import CarCheckerMain
from MechanicGUI import MechanicMain

## init database connection
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

# TODO: Create a function to initialize and return a PostgreSQL connection.

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "username" not in st.session_state:
        st.session_state["username"] = None
    
    if st.session_state['authenticated'] == False and st.session_state["username"] is None:
        login_main()
    else:
        user_id = st.session_state["user_id"]

        # st.write('your user id is',user_id)
        cursor.execute(f'SELECT * FROM account WHERE AID = {str(st.session_state["user_id"])};')
        user_info = cursor.fetchone()

        # user info
        user_type = user_info[4]

        if (user_type == "Seller"):
            SellerMain()
            
        elif(user_type == "Buyer"):
            BuyerMain()

        elif (user_type == "CarChecker"):
            CarCheckerMain()

        elif (user_type == "Mechanic"):
            MechanicMain()

        elif (user_type == "Admin"):
            st.write("You can know access the database directly and see the transactions")



if __name__ == "__main__":
    main()
