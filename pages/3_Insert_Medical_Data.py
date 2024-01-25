import pandas as pd 
import streamlit as st
from supabase import create_client, Client
import numpy as np
import random
from random import randrange
from datetime import timedelta
from datetime import datetime
import json 
import datetime as dt

st.set_page_config(
    page_title="Medory",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Make the connection with Supabase - Database:
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    #client = create_client(url, key)
    return create_client(url, key)
con = init_connection()

def select_all_from_medory_user_table():
    query = con.table("medory_user_table").select("*").execute()
    return query
query = select_all_from_medory_user_table()
df_medory_user_table = pd.DataFrame(query.data)
df_medory_user_table_unique_values = df_medory_user_table.copy()
assign_user = st.selectbox("Αναφορά Χρήστη  " , (df_medory_user_table_unique_values['fullname']))
row_index = df_medory_user_table_unique_values.index[df_medory_user_table_unique_values['fullname']==assign_user].tolist()
user_id = df_medory_user_table_unique_values['id'][df_medory_user_table_unique_values['fullname'] == assign_user].values[0]
# if assign_user != '':
#     df_medory_user_table_unique_values['bmi'] = df_medory_user_table_unique_values['bmi'] = df_medory_user_table_unique_values['weight'] / ((df_medory_user_table_unique_values['height'] / 100) ** 2)
#     st.sidebar.write("Όνομα:", df_medory_user_table_unique_values.loc[row_index[0]]['fullname'])
#     st.sidebar.write("Ηλικία:", df_medory_user_table_unique_values.loc[row_index[0]]['age'])
#     st.sidebar.write("Βάρος:", df_medory_user_table_unique_values.loc[row_index[0]]['weight'])
#     st.sidebar.write("Ύψος:", df_medory_user_table_unique_values.loc[row_index[0]]['height'])
#     st.sidebar.write("BMI:", round(df_medory_user_table_unique_values.loc[row_index[0]]['bmi'],3))

def insert_data_to_medory_blood_test_table(supabase):
    table_cols_list = ['date', 'glu', 'ure', 'cre', 'urca', 'hdl','tri', 'sgot', 'sgpt', 'ygt', 'na', 'k', 'ca', 'fe', 'fer', 'tke', 'b12', 'ctni', 'tsh', 'crp', 'rbc', 'hgb', 'hct', 'mcv', 'mch', 'mchc', 'rdw', 'wbc', 'neu1', 'lym1', 'mon1', 'eos1', 'baso1', 'neu2', 'lym2', 'mon2', 'eos2', 'baso2', 'plt', 'pct', 'mpv', 'pdw', '25oh_d3', 'user_id']
    df_to_list = df['Αποτέλεσμα'].tolist()
    df_to_list.insert(0, date_input)
    df_to_list.append(str(user_id))
    value_dict = dict(zip(table_cols_list, df_to_list))
    for key, value in value_dict.items():
        if value != value:
            value_dict[key] = 'NaN'
    data = supabase.table('medory_blood_test_table').insert(value_dict).execute()
    return data

st.write("#### Εισαγωγή Εξετάσεων")
with st.form("insert_test_exams_form"):
    st.write("Παρακαλώ όπως ανεβάσετε τα δύο αρχεία που χρειάζονται")
    pdf_uploaded_file = st.file_uploader("Επιλέξτε το αρχείο pdf")
    csv_uploaded_file = st.file_uploader("Επιλέξτε το αρχειο csv")
    date_input = st.date_input("Επιλέξτε την ημερομηνία που έγινε η εξέταση",format="DD.MM.YYYY", value=None)
    
    # Serialize the string using the json module 
    #date_input = json.dumps(date_input) 
    submitted = st.form_submit_button("Εισαγωγή τιμων")
    if submitted:
        if csv_uploaded_file is not None and date_input is not None and assign_user != " ":
            # Convert the datetime object to a string in a specific format 
            date_input = date_input.strftime("%d-%m-%Y") 
            df = pd.read_csv(csv_uploaded_file)
            df["Αποτέλεσμα"] = df["Αποτέλεσμα"].str.replace(',','.')
            data = insert_data_to_medory_blood_test_table(con)
            if data is not None:
                st.success('Thank you! A new entry has been inserted')
            else:
                st.warning("There was a problem with this entry, please")
        else:
            st.error("Παρακαλώ όπως συμπληρώσετε όλα τα πεδία (Αναφορά Χρήστη, αρχείο pdf, αρχείο csv και ημερομηνία.)")
        



