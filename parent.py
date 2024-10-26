import streamlit as st
import pandas as pd
import plotly.express as px

FILE_PATH = "attendance.xlsx"

def load_excel(file_path):
    """Load the Excel file."""
    return pd.read_excel(file_path)

def app_parent_view():
    st.title("Student Attendance Viewer for Parents")

    name_input = st.text_input("Enter the student's name")
    rollno_input = st.text_input("Enter the student's roll number")

    df = load_excel(FILE_PATH)

    if name_input and rollno_input:
        student_data = df[(df['name'].str.lower() == name_input.lower()) &
                          (df['rollno'].astype(str) == rollno_input)]

        if not student_data.empty:
            day_columns = [col for col in df.columns if col.startswith('day')]
            total_days = len(day_columns)
            total_present = student_data[day_columns].sum(axis=1).values[0]
            attendance_percentage = (total_present / total_days) * 100

            # Display attendance percentage with visual highlight if below 75%
            if attendance_percentage < 75:
                st.markdown(f"<h2 style='color:red;'>Attendance Percentage: {attendance_percentage:.2f}% 🔴</h2>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 style='color:green;'>Attendance Percentage: {attendance_percentage:.2f}% 🟢</h2>", unsafe_allow_html=True)

            # Display a pie chart visualizing the attendance
            fig = px.pie(values=[total_present, total_days - total_present], names=['Present', 'Absent'],
                         color_discrete_sequence=["green", "red"])
            st.plotly_chart(fig, use_container_width=True)

            # Optional: Display a detailed view of attendance
            if st.checkbox("Show detailed attendance"):
                detailed_attendance = student_data.melt(id_vars=['name', 'rollno'], value_vars=day_columns,
                                                        var_name='Day', value_name='Attendance')
                detailed_attendance['Attendance'] = detailed_attendance['Attendance'].map({1: 'Present', 0: 'Absent'})
                st.dataframe(detailed_attendance)

        else:
            st.warning("No records found. Please check the name and roll number.")

if __name__ == "__main__":
    app_parent_view()
