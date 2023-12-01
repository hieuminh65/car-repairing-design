import streamlit as st
import psycopg2
from config import Config

from login import login_main
from SellerGUI import SellerMain
from BuyerGUI import BuyerMain
from CarCheckerGUI import CarCheckerMain
from MechanicGUI import MechanicMain

db_params = {
    "host": Config.HOST,
    "database": Config.DATABASE,
    "user": Config.USER,
    "password": Config.PASSWORD
}

connection = psycopg2.connect(**db_params)

cursor = connection.cursor()


st.title("Funny Car Shop")

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "username" not in st.session_state:
        st.session_state["username"] = None
    
    if st.session_state['authenticated'] == False and st.session_state["username"] is None:
        login_main()
    else:
        user_id = st.session_state["user_id"]

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


if __name__ == "__main__":
    main()
