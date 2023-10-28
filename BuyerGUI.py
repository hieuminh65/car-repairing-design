import streamlit as st
import psycopg2
import pandas as pd
from config import Config

def fetch_and_display_table(cursor, table_name):
    try:
        if table_name == 'carparts':
            cursor.execute('''SELECT * FROM carparts JOIN carunchecked ON cid = ucid ;''')
        else:
            cursor.execute("""
                SELECT CarUnchecked.UCID, CarUnchecked.description, CarUnchecked.model, 
                    CarUnchecked.year, CarUnchecked.status, CarUnchecked.seller_aid
                FROM greatcar 
                JOIN CarUnchecked ON greatcar.UCID = CarUnchecked.UCID;
            """)
        data = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=colnames)
        st.dataframe(df, width=1080)
        return df  # Return DataFrame for further use
    except Exception as e:
        st.error(f"Error: Unable to fetch data from {table_name}. {e}")

def connect_db(db_params):
    try:
        return psycopg2.connect(**db_params)
    except Exception as e:
        st.error(f"Error: Unable to connect to the database. {e}")
        st.stop()

def BuyerMain():
    user_id = st.session_state.get("user_id", "default_user_id")

    db_params = {
        "host": Config.HOST,
        "database": Config.DATABASE,
        "user": Config.USER,
        "password": Config.PASSWORD
    }

    connection = connect_db(db_params)

    st.title("Car Shop")

    try:
        with connection.cursor() as cursor:
            st.subheader("Available Cars")
            df_cars = fetch_and_display_table(cursor, "greatcar")
            st.subheader("Available Car Parts")
            df_parts = fetch_and_display_table(cursor, "carparts")
    except Exception as e:
        st.error(f"Error: Unable to fetch data from the database. {e}")
        st.stop()

    # Buy a Car
    with st.form(key='buy_car_form'):
        st.write("Buy a Car")
        ucid_to_buy = st.selectbox('Choose the UCID of the car to buy:', df_cars['ucid'].values)
        submit_button_car = st.form_submit_button(label='Buy Car')

        if submit_button_car:
            # Transaction logic for buying a car
            try:
                with connection.cursor() as cursor:
                    sellerId = df_cars[df_cars['ucid'] == ucid_to_buy]['seller_aid']  # Placeholder, implement logic to obtain sellerId
                    gcid = ucid_to_buy  # Placeholder, implement logic to obtain gcid
                    cursor.execute("""
                        INSERT INTO transaction (buyerid, sellerid, gcid)
                        VALUES (%s, %s, %s);
                    """, (int(user_id), int(sellerId), int(gcid)))

                    cursor.execute(f"DELETE FROM greatcar WHERE UCID = {int(ucid_to_buy)} ")
                    connection.commit()
                    st.success(f"You have successfully purchased the car with UCID {ucid_to_buy}.")
                    st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: Unable to complete the purchase. {e}")
                connection.rollback()

    # Buy a Car Part
    with st.form(key='buy_part_form'):
        st.write("Buy a Car Part")

        # part_id_to_buy is actually the UICD in carunchecked
        part_id_to_buy = st.selectbox('Choose the ID of the part to buy:', df_parts['cid'].values)  # Assuming there's a 'PartID' column
        submit_button_part = st.form_submit_button(label='Buy Part')

        sellerId = df_parts[df_parts['cid'] == part_id_to_buy]['seller_aid']

        if submit_button_part:
            # Transaction logic for buying a part
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO transaction (buyerid, sellerid, gcid)
                        VALUES (%s, %s, %s);
                    """, (int(user_id), int(sellerId),int(part_id_to_buy) ))  # Assuming you have a part_transaction table, adjust as needed

                    cursor.execute(f"DELETE FROM carparts WHERE cid = {int(part_id_to_buy)} ")
                    connection.commit()
                    st.success(f"You have successfully purchased the part with ID {part_id_to_buy}.")
                    st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: Unable to complete the purchase. {e}")
                connection.rollback()

    connection.close()

if __name__ == "__main__":
    BuyerMain()
