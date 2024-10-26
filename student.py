import streamlit as st
import pandas as pd
import plotly.express as px

# Path to your Excel file
FILE_PATH = "attendance.xlsx"

# Function to load the Excel file
@st.cache_data
def load_excel(file_path):
    return pd.read_excel(file_path)

# Streamlit app for student view
def app_student_view():
    st.title('Student Attendance Tracker')

    # User input for name and roll number
    name_input = st.text_input('Enter your name')
    rollno_input = st.text_input('Enter your roll number')

    # Load the Excel file
    df = load_excel(FILE_PATH)

    if name_input and rollno_input:
        # Filter the DataFrame for the student's data based on name and roll number
        student_data = df[(df['name'].str.lower() == name_input.lower()) & (df['rollno'].astype(str) == rollno_input)]

        if not student_data.empty:
            # Calculate attendance percentage
            day_columns = [col for col in df.columns if col.startswith('day')]
            total_days = len(day_columns)
            total_present = student_data[day_columns].sum(axis=1).values[0]
            attendance_percentage = (total_present / total_days) * 100

            # Display attendance percentage
            st.write(f'Attendance Percentage: {attendance_percentage:.2f}%')

            # Display student's attendance details and highlight absent days
            student_attendance = student_data.melt(id_vars=['name', 'rollno'], value_vars=day_columns, var_name='Day', value_name='Attendance')
            student_attendance['Attendance'] = student_attendance['Attendance'].map({1: 'Present', 0: 'Absent'})
            absent_days = student_attendance[student_attendance['Attendance'] == 'Absent']
            st.dataframe(absent_days[['Day', 'Attendance']], height=200)

            # Pie chart for overall attendance
            fig = px.pie(values=[total_present, total_days - total_present], names=['Present', 'Absent'],
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error('No records found. Please check your name and roll number.')

# Run the app for student view
if __name__ == "__main__":
    app_student_view()
