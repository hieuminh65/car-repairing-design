import streamlit as st
import psycopg2
from SecurityCheck import check_password_strength, check_email

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

def valid_passwords(username: str, password: str) -> bool:
    """Password must have at least 8 characters, 1 uppercase letter, 1 lowercase letter, and 1 number."""
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(
        char.isupper() for char in password
    ) and any(char.islower() for char in password)


def login_success(message: str, username: str, user_id: int) -> None:
    st.success(message)
    st.session_state["authenticated"] = True
    st.session_state["username"] = username
    st.session_state['user_id'] = user_id

    st.experimental_rerun()


def login_form(
    title: str = "Authentication",
    user_tablename: str = "users",
    username_col: str = "username",
    password_col: str = "password",
    create_title: str = "Create new account",
    login_title: str = "Login to existing account",
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
                    disabled=st.session_state["authenticated"]
                )

                secret_key = st.text_input(label = "Enter the secret key (Only for Admin)", type="password")

                # select type
                user_type = st.radio(
                    "What is your type",
                    ["Seller", "Buyer", "Admin"],
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
                        
                    try:
                        cursor.execute('''INSERT INTO account (username, password, email, type)
                                        VALUES (%s, %s, %s, %s)
                                        RETURNING AID;''',
                                    (username, password, email, user_type))
                        
                        # connection.commit()

                        cursor.execute(f'''SELECT AID FROM Account
                                            ORDER BY AID DESC
                                            LIMIT 1;
                                       ''')
                        
                        latest_account = cursor.fetchone()
                        userid = latest_account[0]

                        if (user_type == 'Seller'):
                            cursor.execute(f'''INSERT INTO Seller (SellerID ,Total_Cars_Sold)
                                            VALUES
                                            ( '{userid}' ,'0');
                                            ''')
                            connection.commit()
                        elif (user_type == 'Buyer'):
                            cursor.execute(f'''INSERT INTO Buyer (BuyerID, Total_Purchases)
                                            VALUES
                                            ('{userid}','0');
                                            ''')
                            connection.commit()
                        
                        elif (user_type == 'Admin'):
                            if secret_key == Config.SECRET_KEY:
                                cursor.execute(f'''INSERT INTO Admin (AdminID)
                                                VALUES
                                                ('{userid}');
                                                ''')
                                connection.commit()
                            else:
                                st.error("Wrong secret key")
                                st.stop()

                        login_success(message=create_success_message, username=username, user_id=userid)
                    except Exception as err:
                        st.error(f'Register unsuccessful ')
                        connection.rollback()
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

                    # TODO: Insert authentication logic for logging into an existing account using PostgreSQL.
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
            create_password_placeholder="⚠️ Password will be stored as plain text. You won't be able to recover it if you forget."
        )