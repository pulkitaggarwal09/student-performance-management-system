import streamlit as st
import sqlite3
import pandas as pd

# Database functions
def create_table():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            course TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_student(name, age, course, email):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, course, email) VALUES (?, ?, ?, ?)", 
                   (name, age, course, email))
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect("students.db")
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

def update_student(id, name, age, course, email):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=?, age=?, course=?, email=? WHERE id=?", 
                   (name, age, course, email, id))
    conn.commit()
    conn.close()

def delete_student(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Streamlit UI
def main():
    st.title("Smart Student Management System")
    menu = ["Add Student", "View Students", "Update Student", "Delete Student"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_table()

    if choice == "Add Student":
        st.subheader("Add Student Details")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        course = st.text_input("Course")
        email = st.text_input("Email")

        if st.button("Add"):
            add_student(name, age, course, email)
            st.success(f"Student {name} added successfully!")

    elif choice == "View Students":
        st.subheader("Student Records")
        df = get_students()
        st.dataframe(df)

    elif choice == "Update Student":
        st.subheader("Update Student Details")
        df = get_students()
        ids = df["id"].tolist()
        selected_id = st.selectbox("Select Student ID", ids)

        if selected_id:
            student = df[df["id"] == selected_id].iloc[0]
            name = st.text_input("Name", student["name"])
            age = st.number_input("Age", min_value=1, max_value=100, step=1, value=student["age"])
            course = st.text_input("Course", student["course"])
            email = st.text_input("Email", student["email"])

            if st.button("Update"):
                update_student(selected_id, name, age, course, email)
                st.success("Student Updated Successfully!")

    elif choice == "Delete Student":
        st.subheader("Delete Student")
        df = get_students()
        ids = df["id"].tolist()
        selected_id = st.selectbox("Select Student ID to Delete", ids)

        if st.button("Delete"):
            delete_student(selected_id)
            st.warning(f"Student with ID {selected_id} deleted!")

if __name__== "__main__":
    main()