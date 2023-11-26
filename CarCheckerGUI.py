import streamlit as st
import psycopg2
import pandas as pd
from config import Config

def CarCheckerMain():
    user_id = st.session_state["user_id"]

    db_params = {
        "host": Config.HOST,
        "database": Config.DATABASE,
        "user": Config.USER,
        "password": Config.PASSWORD
    }

    try:
        connection = psycopg2.connect(**db_params)
    except Exception as e:
        st.error(f"Error: Unable to connect to the database. Check your database credentials. {e}")
        st.stop()

    st.title("Car Accepted")
    
    # Fetch and display data
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM carunchecked WHERE uncheck = True;")
            data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
    except Exception as e:
        st.error(f"Error: Unable to fetch data from the database. {e}")
        st.stop()

    # Creating a dataframe from the fetched data
    df = pd.DataFrame(data, columns=colnames)

    # Drop the 'Uncheck' column from display
    df_display = df.drop(columns=['uncheck'])

    df_display['isCarGood'] = False

    edited_df = st.data_editor(df_display, num_rows="dynamic")

    submitted = st.button("Submit", type="secondary")
    
    if submitted:
        try:
            with connection.cursor() as cursor:
                for index, row in edited_df.iterrows():
                    
                    if row['isCarGood']:
                        # Placeholder for action when 'isCarGood' is True
                        st.write(f"ID {row['ucid']} is True. Do something here.")
                        
                        # Write SQL query to add to greatcar table
                        cursor.execute(f"""
                            INSERT INTO greatcar (ucid, checkerid)
                            VALUES ( {int(row['ucid'])}, {int(user_id)} );
                        """)
        
                    else:
                        # Placeholder for action when 'isCarGood' is False
                        st.write(f"ID {row['ucid']} is False. Do something else here.")

                        # query to add to BrokenCar
                        cursor.execute(f"""
                            INSERT INTO brokencar (ucid, checkerid)
                            VALUES ( {int(row['ucid'])}, {int(user_id)} );
                        """)
                        
                # Updating all 'Uncheck' values to False
                cursor.execute("UPDATE carunchecked SET uncheck = False WHERE uncheck = True;")
                connection.commit()

        except Exception as e:
            st.error(f"Error: Unable to update the database. {e}")

        finally:
            # Refetching the data after the update
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM carunchecked WHERE uncheck = True;")
                    data = cursor.fetchall()
                    colnames = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(data, columns=colnames)
                    df_display = df.drop(columns=['uncheck'])
                    df_display['isCarGood'] = False
                    st.table(df_display)
            except Exception as e:
                st.error(f"Error: Unable to fetch the updated data. {e}")
