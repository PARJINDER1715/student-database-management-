import streamlit as st
import sqlite3

# Database Functions
DB_NAME = "student.db"

def init_db():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY,
                StdID TEXT,
                Firstname TEXT,
                Surname TEXT,
                DoB TEXT,
                Age TEXT,
                Gender TEXT,
                Address TEXT,
                Mobile TEXT
            )
        """)
        con.commit()

def add_student(StdID, Firstname, Surname, DoB, Age, Gender, Address, Mobile):
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO student (StdID, Firstname, Surname, DoB, Age, Gender, Address, Mobile)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (StdID, Firstname, Surname, DoB, Age, Gender, Address, Mobile))
        con.commit()

def get_all_students():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM student")
        return cur.fetchall()

def delete_student(id):
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM student WHERE id=?", (id,))
        con.commit()

def update_student(id, StdID, Firstname, Surname, DoB, Age, Gender, Address, Mobile):
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("""
            UPDATE student SET StdID=?, Firstname=?, Surname=?, DoB=?, Age=?, Gender=?, Address=?, Mobile=?
            WHERE id=?
        """, (StdID, Firstname, Surname, DoB, Age, Gender, Address, Mobile, id))
        con.commit()

def search_students(StdID, Firstname, Surname, DoB, Age, Gender, Address, Mobile):
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT * FROM student WHERE StdID=? OR Firstname=? OR Surname=? OR DoB=? OR Age=? OR Gender=? OR Address=? OR Mobile=?
        """, (StdID, Firstname, Surname, DoB, Age, Gender, Address, Mobile))
        return cur.fetchall()

# Streamlit UI
st.set_page_config(page_title="Student DB", layout="centered")
st.title("Student Database Management System")

init_db()

menu = ["Add", "View", "Search", "Update", "Delete"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add":
    st.subheader("Add New Student")
    StdID = st.text_input("Student ID")
    Firstname = st.text_input("Firstname")
    Surname = st.text_input("Surname")
    DoB = st.date_input("Date of Birth")
    Age = st.text_input("Age")
    Gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    Address = st.text_input("Address")
    Mobile = st.text_input("Mobile")

    if st.button("Add Student"):
        add_student(StdID, Firstname, Surname, str(DoB), Age, Gender, Address, Mobile)
        st.success("Student added successfully")

elif choice == "View":
    st.subheader("View All Students")
    students = get_all_students()
    for row in students:
        st.write(row)

elif choice == "Search":
    st.subheader("Search Student")
    StdID = st.text_input("Student ID")
    Firstname = st.text_input("Firstname")
    Surname = st.text_input("Surname")
    DoB = st.text_input("Date of Birth")
    Age = st.text_input("Age")
    Gender = st.text_input("Gender")
    Address = st.text_input("Address")
    Mobile = st.text_input("Mobile")

    if st.button("Search"):
        results = search_students(StdID, Firstname, Surname, DoB, Age, Gender, Address, Mobile)
        for row in results:
            st.write(row)

elif choice == "Update":
    st.subheader("Update Student Record")
    students = get_all_students()
    student_ids = {f"{s[0]} - {s[1]} {s[2]}": s[0] for s in students}
    selected = st.selectbox("Select student", list(student_ids.keys()))
    sid = student_ids[selected]

    student = [s for s in students if s[0] == sid][0]
    StdID = st.text_input("Student ID", student[1])
    Firstname = st.text_input("Firstname", student[2])
    Surname = st.text_input("Surname", student[3])
    DoB = st.text_input("Date of Birth", student[4])
    Age = st.text_input("Age", student[5])
    Gender = st.text_input("Gender", student[6])
    Address = st.text_input("Address", student[7])
    Mobile = st.text_input("Mobile", student[8])

    if st.button("Update"):
        update_student(sid, StdID, Firstname, Surname, DoB, Age, Gender, Address, Mobile)
        st.success("Record updated successfully")

elif choice == "Delete":
    st.subheader("Delete Student Record")
    students = get_all_students()
    student_ids = {f"{s[0]} - {s[1]} {s[2]}": s[0] for s in students}
    selected = st.selectbox("Select student", list(student_ids.keys()))
    sid = student_ids[selected]

    if st.button("Delete"):
        delete_student(sid)
        st.success("Record deleted successfully")
