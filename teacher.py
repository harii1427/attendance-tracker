import streamlit as st
import pandas as pd
import plotly.express as px

# Path to your Excel file
FILE_PATH = "attendance.xlsx"

def load_excel(file_path):
    """Load the Excel file."""
    return pd.read_excel(file_path)

def save_excel(df, file_path):
    """Save the DataFrame back to the Excel file."""
    df.to_excel(file_path, index=False)

def add_new_student(df, name, rollno):
    """Add a new student to the DataFrame."""
    new_row = {col: 0 for col in df.columns if col.startswith('day')}
    new_row['name'] = name
    new_row['rollno'] = rollno
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

def app():
    st.title('Attendance Details')

    df = load_excel(FILE_PATH)  # Load the DataFrame

    # Add new student section
    with st.expander("Add New Student"):
        new_student_name = st.text_input("Student's Name", key="new_student_name")
        new_student_rollno = st.text_input("Student's Roll No", key="new_student_rollno")
        if st.button("Add Student") and new_student_name and new_student_rollno:
            df = add_new_student(df, new_student_name, new_student_rollno)
            save_excel(df, FILE_PATH)
            st.success(f"New student {new_student_name} added successfully.")
            df = load_excel(FILE_PATH)  # Reload the DataFrame

    # Display and update attendance
    day_columns = [col for col in df.columns if col.startswith('day')]
    selected_day = st.selectbox("Select Day", options=day_columns)

    search_query = st.text_input('Search by name or roll number')

    def filter_data(data, query):
        """Filter data based on search query."""
        if query.isdigit():
            return data[data['rollno'].astype(str).str.contains(query)]
        else:
            return data[data['name'].str.contains(query, case=False)]

    if search_query:
        filtered_df = filter_data(df[['name', 'rollno'] + day_columns], search_query)
    else:
        filtered_df = df[['name', 'rollno'] + day_columns]

    if not filtered_df.empty and selected_day:
        st.dataframe(filtered_df[['name', 'rollno', selected_day]])

        present_count = filtered_df[selected_day].sum()
        absent_count = len(filtered_df) - present_count
        fig = px.pie(values=[present_count, absent_count], names=['Present', 'Absent'],
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

    # Add a new day section
    new_day = f"day{len(day_columns) + 1}"
    if st.button(f"Add {new_day}"):
        df[new_day] = 0  # Initialize everyone as absent for the new day
        save_excel(df, FILE_PATH)
        st.success(f"{new_day} added successfully.")
        df = load_excel(FILE_PATH)  # Reload the DataFrame

    # Mark attendance for an existing or new day
    day_to_mark = st.selectbox("Mark attendance for:", [None] + day_columns + [new_day], key='day_to_mark')
    if day_to_mark:
        for index, row in df.iterrows():
            present = st.checkbox(f"{row['name']} (Roll No: {row['rollno']})", key=f"{index}_{day_to_mark}", value=row[day_to_mark]==1)
            df.at[index, day_to_mark] = int(present)
        if st.button("Update Attendance", key='update_attendance'):
            save_excel(df, FILE_PATH)
            st.success("Attendance updated.")
            df = load_excel(FILE_PATH)  # Reload the DataFrame after updating

if __name__ == "__main__":
    app()
