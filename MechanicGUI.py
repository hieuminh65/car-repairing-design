import streamlit as st
import psycopg2
import pandas as pd
from config import Config


def MechanicMain():
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
        st.error(f"Error: Unable to connect to the database. {e}")
        st.stop()

    st.title("Mechanic View")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT carunchecked.ucid, carunchecked.description, carunchecked.model, carunchecked.year, carunchecked.status FROM brokencar JOIN carunchecked on brokencar.UCID = carunchecked.UCID;")
            data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
    except Exception as e:
        st.error(f"Error: Unable to fetch data from the database. {e}")
        st.stop()

    df = pd.DataFrame(data, columns=colnames)

    df['carPart'] = ''
    df['isFixable'] = False

    edited_df = st.data_editor(df, num_rows="dynamic")

    submitted = st.button("Submit", type="secondary")
    
    if submitted:
        try:
            with connection.cursor() as cursor:
                for index, row in edited_df.iterrows():
                    
                    if row['isFixable']:
                        
                        cursor.execute(f"""
                            INSERT INTO greatcar (ucid)
                            VALUES ( {int(row['ucid'])} );
                        """)

                        cursor.execute(
                            """
                            DELETE FROM brokencar 
                            WHERE ucid = %s;
                            """,
                            (int(row['ucid']),)
                        )

                    else:
                        st.write('car part', row["carPart"])
                        cursor.execute(f"""
                            INSERT INTO CarParts (cid, mechanicid, partname)
                            VALUES ( {int(row['ucid'])}, {int(user_id)}, 'To be updated...' );
                        """)

                        cursor.execute(
                            """
                            DELETE FROM brokencar 
                            WHERE ucid = %s;
                            """,
                            (int(row['ucid']),)
                        )

                connection.commit()

        except Exception as e:
            st.error(f"Error: Unable to update the database. {e}")

        finally:
            print()

    back = st.button(":back:", type="secondary")
    if back:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()

