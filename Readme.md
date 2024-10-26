# Unified Attendance System

This project provides an attendance management system designed to cater to different user roles: Students, Parents, and Teachers. Each role has a dedicated Streamlit interface that offers tailored functionalities.

## System Components

The system comprises three separate Streamlit interfaces:

- `student.py`: Interface for students to view their attendance records and other student-specific information.
- `parent.py`: Interface for parents to monitor their child's attendance, with insights and analytics.
- `teacher.py`: Interface for teachers to manage attendance records, including adding new students, marking attendance, and other administrative functionalities.

## Getting Started

Before running any of the interfaces, ensure you have Python and Streamlit installed on your system. If Streamlit is not installed, you can install it using pip:

```bash
pip install streamlit

## For Students:

```bash
streamlit run student.py


## For Teachers:

```bash
streamlit run teacher.py


## For Parent:

```bash
streamlit run parent.py



## Features
Each interface provides role-specific functionalities:

Student Interface: View attendance, submit excuses, etc.
Parent Interface: Monitor child's attendance, access reports and analytics.
Teacher Interface: Add or remove students, mark attendance, generate reports.

