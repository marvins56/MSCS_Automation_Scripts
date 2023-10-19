# import streamlit as st
# import random
# import os

# # Shift types
# shift_types = ["Normal Day", "Long Day", "Night Shift"]
# filename = "shifts.txt"

# def generate_shifts(doctors, num_days):
#     shifts = {}
#     for day in range(1, num_days + 1):
#         random.shuffle(doctors)
#         shifts[f"Day {day}"] = {doc: random.choice(shift_types) for doc in doctors}
#     return shifts

# def save_shifts_to_file(shifts):
#     with open(filename, "w") as file:
#         for day, assignments in shifts.items():
#             file.write(day + "\n")
#             for doctor, shift in assignments.items():
#                 file.write(f"{doctor}: {shift}\n")
#             file.write("-" * 40 + "\n")

# st.title("Doctors' Shifts Scheduler")

# # Sidebar selection
# options = ["Generate Shifts", "View Current Shifts"]
# choice = st.sidebar.selectbox("Choose an option", options)

# if choice == "Generate Shifts":
#     # Input number of doctors and their names
#     num_doctors = st.number_input("Number of doctors", min_value=1, value=5)
#     doctors = [st.text_input(f"Doctor {i+1} Name", f"Doctor {i+1}") for i in range(num_doctors)]

#     # Input number of days to generate shifts for
#     num_days = st.number_input("Number of days", min_value=1, value=7)

#     if st.button("Generate Shifts"):
#         shifts = generate_shifts(doctors, num_days)
#         for day, assignments in shifts.items():
#             st.write(day)
#             for doctor, shift in assignments.items():
#                 st.write(f"{doctor}: {shift}")
        
#         # Save the shifts to a file
#         save_shifts_to_file(shifts)
#         st.success("Shifts saved successfully!")

# elif choice == "View Current Shifts":
#     if os.path.exists(filename):
#         with open(filename, "r") as file:
#             st.text(file.read())
#     else:
#         st.warning("No shifts data found. Please generate shifts first.")
import streamlit as st
import random
import os
import pandas as pd
import plotly.express as px

# Shift types
shift_types = ["Normal Day", "Long Day", "Night Shift"]
filename = "shifts.txt"

def generate_shifts(doctors, num_days):
    shifts = {}
    for day in range(1, num_days + 1):
        random.shuffle(doctors)
        shifts[f"Day {day}"] = {doc: random.choice(shift_types) for doc in doctors}
    return shifts

def save_shifts_to_file(shifts):
    with open(filename, "w") as file:
        for day, assignments in shifts.items():
            file.write(day + "\n")
            for doctor, shift in assignments.items():
                file.write(f"{doctor}: {shift}\n")
            file.write("-" * 40 + "\n")

st.title("Doctors' Shifts Scheduler")

# Sidebar selection
options = ["Generate Shifts", "View Current Shifts"]
choice = st.sidebar.selectbox("Choose an option", options)

if choice == "Generate Shifts":
    # Input number of doctors and their names
    num_doctors = st.number_input("Number of doctors", min_value=1, value=5)
    doctors = [st.text_input(f"Doctor {i+1} Name", f"Doctor {i+1}") for i in range(num_doctors)]

    # Input number of days to generate shifts for
    num_days = st.number_input("Number of days", min_value=1, value=7)

    if st.button("Generate Shifts"):
        shifts = generate_shifts(doctors, num_days)
        shift_df = pd.DataFrame(shifts)

        # Visualize Shift Distribution
        st.subheader("Shift Distribution")
        shift_count = shift_df.apply(lambda x: x.value_counts())
        fig = px.bar(shift_count, title="Shift Distribution", labels={'index': 'Shift Type', 'value': 'Count'})
        st.plotly_chart(fig)

        # Interactive Calendar View
        st.subheader("Shift Calendar")
        st.write(shift_df)

        # Save the shifts to a file
        save_shifts_to_file(shifts)
        st.success("Shifts saved successfully!")

elif choice == "View Current Shifts":
    if os.path.exists(filename):
        with open(filename, "r") as file:
            st.text(file.read())
    else:
        st.warning("No shifts data found. Please generate shifts first.")
