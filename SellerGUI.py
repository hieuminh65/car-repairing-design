import streamlit as st
import psycopg2


def SellerMain():
    user_id = st.session_state["user_id"]

    db_params = {
        "host": "localhost",
        "database": "final_project",
        "user": "postgres",
        "password": "Toanposgre"
    }

    # Setup a connection. Always remember to handle connection exceptions in production code
    try:
        connection = psycopg2.connect(**db_params)
    except Exception as e:
        st.error(f"Error: Unable to connect to the database. Check your database credentials. {e}")
        st.stop()

    st.title("Car Data Entry Form")

    # Create a form
    with st.form(key='car_form'):
        st.write("Please enter the following details:")

        # Collecting User Inputs
        description = st.text_area(label="Description", help="Enter a detailed description of the car.")
        model = st.text_input(label="Model", help="Enter the car model.")
        year = st.number_input(label="Year", min_value=1900, max_value=2023,
                               help="Enter the manufacture year of the car.")
        status_options = ["New", "Used", "Damaged"]
        status = st.selectbox(label="Status", options=status_options, help="Select the current status of the car.")

        # Submit Button
        submit_button = st.form_submit_button(label="Submit Car Data")

        if submit_button:
                try:
                    with connection.cursor() as cursor:
                        # Align the UCID sequence
                        align_sequence_query = "SELECT setval(pg_get_serial_sequence('carunchecked', 'ucid'), (SELECT COALESCE(MAX(UCID), 0) FROM CarUnchecked) + 1, false);"
                        cursor.execute(align_sequence_query)

                        # Insert query
                        insert_query = '''INSERT INTO CarUnchecked (Description, Model, Year, Status, Seller_AID, uncheck)
                                          VALUES (%s, %s, %s, %s, %s, TRUE)
                                          RETURNING *;'''
                        cursor.execute(insert_query, (description, model, year, status, user_id))

                        latest_row = cursor.fetchone()
                        if latest_row is not None:
                            # Process the latest_row data
                            connection.commit()
                            st.success("Data successfully inserted into the database.")
                        else:
                            st.error("Error: No data returned from the INSERT operation.")
                except Exception as e:
                    st.error(f"Error: Unable to insert data into the database. {e}")
