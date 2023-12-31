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

    st.title("Cars Waitlist")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM carunchecked WHERE uncheck = TRUE;")
            data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
    except Exception as e:
        st.error(f"Error: Unable to fetch data from the database. {e}")
        st.stop()

    df = pd.DataFrame(data, columns=colnames)

    df_display = df.drop(columns=['uncheck'])

    df_display['isCarGood'] = False

    edited_df = st.data_editor(df_display, num_rows="dynamic")

    submitted = st.button("Submit", type="secondary")
    
    if submitted:
        try:
            with connection.cursor() as cursor:
                for index, row in edited_df.iterrows():
                    
                    if row['isCarGood']:

                        cursor.execute(f"""
                            INSERT INTO greatcar (ucid)
                            VALUES ( {int(row['ucid'])} );
                        """)
        
                    else:

                        cursor.execute(f"""
                            INSERT INTO brokencar (ucid)
                            VALUES ( {int(row['ucid'])});
                        """)
                        
                cursor.execute("UPDATE carunchecked SET uncheck = False WHERE uncheck = True;")
                connection.commit()

        except Exception as e:
            st.error(f"Error: Unable to update the database. {e}")



    back = st.button(":back:", type="secondary")
    if back:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()

