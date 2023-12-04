import streamlit as st
import pandas as pd
import json
import plotly.express as px
import datetime

def detail_about_your_weight(df):
    st.write(df)
    # Ensure 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Convert 'weight' column to numeric type, handling non-convertible values as NaN
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce')

    # Sort DataFrame by 'date' column in descending order
    df = df.sort_values('date', ascending=True)  # Ensure the data is sorted in ascending order for plotting

    # Isolate the last two dates' weights
    last_two_weights = df.tail(2)['weight'].tolist()  # Using tail(2) to get the last 2 records

    if len(last_two_weights) == 2:
        earliest_weight = last_two_weights[0]  # Second last weight
        latest_weight = last_two_weights[1]  # Latest weight
        weight_change = latest_weight - earliest_weight

        if weight_change != 0:
            percentage_change = (weight_change / abs(earliest_weight)) * 100 if earliest_weight != 0 else 0

            if weight_change > 0:
                st.write(f"Weight has increased by {weight_change:.2f} units.")
                st.write(f"This is a {percentage_change:.2f}% increase since the second last record.")
            else:
                st.write(f"Weight has decreased by {-weight_change:.2f} units.")
                st.write(f"This is a {-percentage_change:.2f}% decrease since the second last record.")
        else:
            st.write("Weight remains unchanged")
        
        # Plotting weekly weight trend
        

    else:
        st.write("Insufficient data to calculate weight change for the last two days.")

    six_months_ago = datetime.date.today() - pd.DateOffset(months=6)
    filtered_df = df[df['date'] >= six_months_ago]

    # Visualization of weight trends for the last 6 months using Plotly
    if not filtered_df.empty:
        fig = px.line(filtered_df, x='date', y='weight', title='Weight Trends for Last 6 Months')
        st.plotly_chart(fig)
    else:
        st.write("No data available for the last 6 months.")







def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if not isinstance(data, list):
            data = []
    return data

def update_data(file_path, new_data):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = [] 
    except FileNotFoundError:
        data = []
    
    data.append(new_data)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        

def update_page():
    st.title("Update you latest Weight")

    file_path = 'weight.json'
    data = load_data(file_path)
    df = pd.DataFrame(data)

    name_list = df['Name'].tolist()
    name_list = list(set(name_list)) 
    name_list.append("I want to add my name")

    selected_name = st.selectbox("Select a Name", name_list)
    if selected_name == "I want to add my name":
        name = st.text_input("Enter your Name", key="name_input")
        password=st.text_input("Create you password")
    else:
        name = selected_name

    latest_weight = st.number_input("Enter your latest weight", value=None, placeholder="Type a number...")
    current_date = datetime.date.today()
    if st.button("Update"):
        if latest_weight is not None and name != "":
            new_data = {
                "Name": str(name),
                "date": str(current_date),
                "weight": latest_weight
            }
            update_data(file_path, new_data)
            if selected_name == "I want to add my name":
                password_new_data = {
                    "Name": str(name),
                    "password": str(password)
                }
                update_data("password.json", password_new_data)
            st.success("Your Data is Updated")
        else:
            st.error("Please check your name and weight")

def you_details():
    st.title("See Your Weight Trends")

    file_path = 'weight.json'
    data = load_data(file_path)

    passs_data=load_data("password.json")

    df_pass=pd.DataFrame(passs_data)

    df = pd.DataFrame(data)

    name_list = df['Name'].tolist()
    name_list = list(set(name_list)) 

    selected_name = st.selectbox("Select a Name", name_list)
    password=st.text_input("Enter your password",type="password")


    if st.button("Apply Filter"):
        selected_row=df_pass[df_pass["Name"]==selected_name] 
        selected_password = selected_row.iloc[0]['password']
        if selected_password==password:
            df_selected = df[df["Name"] == selected_name]
            detail_about_your_weight(df_selected)
        else:
            st.error("Please enter correct Details")

# Sidebar to select page
selected_page = st.sidebar.radio("Select Page", ["Update Data", "See you Weight Trends"])

# Display selected page
if selected_page == "Update Data":
    update_page()
elif selected_page == "See you Weight Trends":
    you_details()
