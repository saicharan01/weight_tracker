import streamlit as st
import pandas as pd
import json
import datetime
import plotly.express as px

def detail_about_your_weight(df):
    st.write(df)
    df['date'] = pd.to_datetime(df['date'])
    earliest_weight = df['weight'].iloc[-1] if not df.empty else None
    latest_weight = df['weight'].iloc[0] if not df.empty else None
    weight_change = latest_weight - earliest_weight if earliest_weight is not None and latest_weight is not None else None
    if weight_change is not None:
        percentage_change = (weight_change / earliest_weight) * 100 if earliest_weight != 0 else 0
        if weight_change > 0:
            st.write(f"Weight has increased by {weight_change:.2f} units.")
            st.write(f"This is a {percentage_change:.2f}% increase since the earliest record.")
        elif weight_change < 0:
            st.write(f"Weight has decreased by {-weight_change:.2f} units.")
            st.write(f"This is a {-percentage_change:.2f}% decrease since the earliest record.")
        else:
            st.write("Weight remains unchanged.")
    else:
        st.write("Insufficient data to calculate weight change.")
    six_months_ago = datetime.date.today() - pd.DateOffset(months=6)
    filtered_df = df[df['date'] >= six_months_ago]
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
    st.title("Update Weight Data")

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
    #current_date = datetime.date.today()
    current_date="2023-10-02"
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
            st.write(df_selected)
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
