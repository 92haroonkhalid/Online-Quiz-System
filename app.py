import streamlit as st
import sqlite3
import hashlib

con = sqlite3.connect("Online Quiz System/database/users.db")
pul = con.cursor()
pul.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
    )
""")
con.commit()
con.close()

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def reg():
    st.title("Registration Page")
    con = sqlite3.connect("Online Quiz System/database/users.db")
    pul = con.cursor()

    name = st.text_input("Name", placeholder="Enter your name")
    email = st.text_input("Email", placeholder="Enter your email").strip().lower()
    pas = st.text_input("Password", placeholder="Enter your password", key="password", type="password")

    if st.button("Register"):
        if email=="" or "." not in email and "@" not in email and "gmail.com" not in email:
            st.error("Invalid email address")
            return
        try:
            pul.execute("INSERT INTO users (username, email, password) values (?, ?, ?, ?)",
                        (name, email, hash_pass(pas)))
            con.commit()
            st.success(f"User registered successfuly as{name}")
        except sqlite3.IntegrityError:
            st.error("Username already exists")
        finally:
            con.close()

def login():
    st.title("Login Page")
    email = st.text_input("Email adrress", placeholder="Enter your email").strip().lower()
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    if st.button("Login"):
        if email=="" or password=="":
            st.error("Please enter email and password")
            return
        con = sqlite3.connect("Online Quiz System/database/users.db")
        pul = con.cursor()
        pul.execute("""
            SELECT username,password
                    FROM users
                    WHERE email = ?
                    """, (email,))
        data = pul.fetchone()
        con.close()

        if data is None:
            st.error("Data is not found")
            return

        if data[1] == hash_pass(password):
            st.success(f"Logged in successfully as {data[0]}")
            st.session_state.user = data[0]
            st.session_state.logedin = True
        else:
            st.error("Invalid credentials")

def questions():
    st.title("Online Quiz")
    st.write("Here is online quiz system.Here you have 10 questions to answer and result will be shown after completion immediately.")

    Q_ans = []
    Q1 = st.text_input("Which planet is known as the Red Planet?", placeholder="Enter your answer").lower() 
    Q_ans.append(Q1)
    Q2 = st.number_input("How many continents are there on Earth?", placeholder="Enter your answer", step=1)
    Q_ans.append(Q2)
    Q3 = st.text_input("What is the largest ocean in the world?", placeholder="Enter your answer").lower()
    Q_ans.append(Q3)
    Q4 = st.text_input("Who painted the Mona Lisa?", placeholder="Enter your answer").lower()
    Q_ans.append(Q4)
    Q5 = st.number_input("In which year did World War II end?", placeholder="Enter your answer", step=1)
    Q_ans.append(Q5)
    Q6 = st.text_input("What is the chemical symbol for Gold?", placeholder="Enter your answer").lower()
    Q_ans.append(Q6)
    Q7 = st.text_input("Which country is known as the Land of the Rising Sun?", placeholder="Enter your answer").lower()
    Q_ans.append(Q7)
    Q8 = st.number_input("How many bones are in the adult human body?", placeholder="Enter your answer", step=1)
    Q_ans.append(Q8)
    Q9 = st.text_input("What is the hardest natural substance on Earth?", placeholder="Enter your answer").lower()
    Q_ans.append(Q9)
    Q10 = st.text_input("What is the largest mammal on Earth?", placeholder="Enter your answer").lower()
    Q_ans.append(Q10)

    ans = ["mars",7,"pacific ccean","leonardo da vinci",1945,"au","japan",206]
    result = 0
    if st.button("Complete"):
        for i in range(len(ans)):
            if Q_ans[i] == ans[i]:
                result += 1

def main():
    st.set_page_config(page_title="Placement Predictor", layout="wide")
    st.title("Student Placement & Salary Prediction App")
    if "logedin" not in st.session_state:
        st.session_state.logedin = False

    st.sidebar.title("Navigation")

    page = st.sidebar.radio("Go to", ["Dashboard","Login", "Register", "Logout"])

    if page == "Login":
        login()

    elif page == "Register":
        reg()

    elif page == "Dashboard":
        if st.session_state.logedin == True:
            st.write(f"Logged in as {st.session_state.user}")
            questions()
        else:    
            st.warning("Please login to access the dashboard.")
            return

    elif page == "Logout":
        st.session_state.clear()
        st.success("Logged out successfully")

main()