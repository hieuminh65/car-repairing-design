import streamlit as st
import psycopg2
from config import Config
from SecurityCheck import check_password_strength, check_email


db_params = {
    "host": Config.HOST,
    "database": Config.DATABASE,
    "user": Config.USER,
    "password": Config.PASSWORD
}

connection = psycopg2.connect(**db_params)

cursor = connection.cursor()


def login_success(message: str, username: str, user_id: int) -> None:
    st.success(message)
    st.session_state["authenticated"] = True
    st.session_state["username"] = username
    st.session_state['user_id'] = user_id

    st.rerun()


def login_form(
    title: str = "Authentication",
    user_tablename: str = "users",
    username_col: str = "username",
    password_col: str = "password",
    create_title: str = "Create new account",
    login_title: str = "Login to existing account",
    allow_guest: bool = False,
    guest_title: str = "Guest login :ninja: ",
    create_username_label: str = "Create a unique username",
    create_email_label: str = "Create a unique email",
    create_email_placeholder: str = "Create a unique email",
    create_username_placeholder: str = None,
    create_username_help: str = None,
    create_password_label: str = "Create a password",
    create_password_placeholder: str = None,
    create_password_help: str = "⚠️ Password will be stored as plain text. Do not reuse from other websites. Password cannot be recovered.",
    create_submit_label: str = "Create account",
    create_success_message: str = "Account created :tada:",
    login_username_label: str = "Enter your unique username",
    login_username_placeholder: str = None,
    login_username_help: str = None,
    login_password_label: str = "Enter your password",
    login_password_placeholder: str = None,
    login_password_help: str = None,
    login_submit_label: str = "Login",
    login_success_message: str = "Login succeeded :tada:",
    login_error_message: str = "Wrong username/password :x: ",
) -> None:
    """Creates a user login form in Streamlit apps.

    Sets `session_state["authenticated"]` to True if the login is successful.
    Sets `session_state["username"]` to provided username for new or existing user, and to `None` for guest login.
    """

    # User Authentication
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "username" not in st.session_state:
        st.session_state["username"] = None

    with st.expander(title, expanded=not st.session_state["authenticated"]):
        create_tab, login_tab = st.tabs(
            [
                create_title,
                login_title,
            ]
        )

        # Create new account
        with create_tab:
            with st.form(key="create"):
                username = st.text_input(
                    label=create_username_label,
                    placeholder=create_username_placeholder,
                    help=create_username_help,
                    disabled=st.session_state["authenticated"],
                )

                email = st.text_input(
                    label=create_email_label,
                    placeholder=create_email_placeholder,
                    help=create_username_help,
                    disabled=st.session_state["authenticated"],
                )

                password = st.text_input(
                    label=create_password_label,
                    placeholder=create_password_placeholder,
                    help=create_password_help,
                    type="password",
                    disabled=st.session_state["authenticated"],
                )

                 # select type
                user_type = st.radio(
                    "What is your type",
                    ["Seller", "Buyer",],
                    horizontal=True
                )


                if st.form_submit_button(
                    label=create_submit_label,
                    type="primary",
                    disabled=st.session_state["authenticated"],
                ):  
                    if email == '' or not check_email(email):
                        st.error("Please fill in your correct email")
                        st.stop()

                    if not check_password_strength(password):
                        st.error('Please use a stronger password with at least 8 characters long, 1 alphabets, 1 numbers, and 1 special character', icon="🚨")
                        st.stop()

                    # TODO: Insert authentication logic for creating a new account using PostgreSQL.
                    try:
                        cursor.execute('''INSERT INTO account (username, password, email, type)

                                          VALUES (%s, %s, %s, %s)
                                          RETURNING AID;''',
                                       (username, password, email, user_type))

                        user_id = cursor.fetchone()[0]

                        # add to the seller/buyer table
                        if user_type == 'Seller':
                            cursor.execute(f'''INSERT INTO Seller (SellerID ,Total_Cars_Sold)
                                            VALUES
                                            ( '{user_id}' ,'0');
                                            ''')
                            connection.commit()
                        else:
                            cursor.execute(f'''INSERT INTO Buyer (BuyerID, Total_Purchases)
                                            VALUES
                                            ('{user_id}','0');
                                            ''')
                            connection.commit()



                        login_success(message=create_success_message, username=username, user_id=user_id)
                    except Exception as err:
                        st.error(f'Register unsuccessful ')
                        st.write(err)

        # Login to existing account
        with login_tab:
            with st.form(key="login"):
                username = st.text_input(
                    label=login_username_label,
                    placeholder=login_username_placeholder,
                    help=login_username_help,
                    disabled=st.session_state["authenticated"],
                )

                password = st.text_input(
                    label=login_password_label,
                    placeholder=login_password_placeholder,
                    help=login_password_help,
                    type="password",
                    disabled=st.session_state["authenticated"],
                )


                if st.form_submit_button(
                    label=login_submit_label,
                    disabled=st.session_state["authenticated"],
                    type="primary",
                ):

                    cursor.execute('SELECT EXISTS(SELECT 1 FROM account WHERE username = %s);', (username,))
                    checked_user_exists = cursor.fetchone()[0]


                    if not checked_user_exists:
                        st.error("You have not sign up")
                    else:
                        cursor.execute(f'''SELECT EXISTS(SELECT 1 FROM account WHERE username = '{username}' AND password = '{password}');''')
                        password_correct = cursor.fetchone()[0]

                        if not password_correct:
                            st.error("Please create a new account or try to remember your password :)) ")
                        
                        else:
                            cursor.execute(f'''SELECT AID FROM Account WHERE Username = '{username}' AND Password = '{password}';''')
                            user_id = cursor.fetchone()[0]

                            login_success(login_success_message, username, user_id=user_id )

def login_main():
    if st.session_state['authenticated'] == True and st.session_state["username"] is not None:
        st.write(f'Welcome back, {st.session_state["username"]}')
    else:
        login_form(
            create_username_placeholder="Username will be visible in the global leaderboard.",
            create_password_placeholder="⚠️ Password will be stored as plain text. You won't be able to recover it if you forget.",
        )