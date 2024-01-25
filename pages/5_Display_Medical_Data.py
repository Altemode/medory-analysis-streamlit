import pandas as pd 
import numpy as np
import streamlit as st
from supabase import create_client, Client
import plotly.express as px
import plotly.graph_objects as go
import datetime
import gettext
from functools import reduce
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import datetime


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

#--------------------------------Fetch all users from database and assign user--------------------------------#
def select_all_from_medory_user_table():
    query = con.table("medory_user_table").select("*").execute()
    df_medory_user_table = pd.DataFrame(query.data)
    assign_user = st.selectbox("Αναφορά Χρήστη  " , (df_medory_user_table['fullname']))
    row_index = df_medory_user_table.index[df_medory_user_table['fullname']==assign_user].tolist()
    # if assign_user != ' ':
    #     df_medory_user_table['bmi'] = df_medory_user_table['bmi'] = df_medory_user_table['weight'] / ((df_medory_user_table['height'] / 100) ** 2)
    #     st.sidebar.write("Όνομα:", df_medory_user_table.loc[row_index[0]]['fullname'])
    #     st.sidebar.write("Ηλικία:", df_medory_user_table.loc[row_index[0]]['age'])
    #     st.sidebar.write("Βάρος:", df_medory_user_table.loc[row_index[0]]['weight'])
    #     st.sidebar.write("Ύψος:", df_medory_user_table.loc[row_index[0]]['height'])
    #     st.sidebar.write("BMI:", round(df_medory_user_table.loc[row_index[0]]['bmi'],3))
    #row_index[0]
    return row_index
#-----------------------------------End of Fetch all users from database -------------------------------------#

#-----------------------------------Fetch all data from database for assigned user -------------------------------------#
def select_all_from_medory_blood_test_table(row_index):
    if row_index[0] >= 1:
        query = con.table("medory_blood_test_table").select("*").eq("user_id", row_index[0]).execute()
        df = pd.DataFrame(query.data)
        dict_columns_names = {
            # for df_medory_general_blood_tests_table
            'rbc' : 'RBC Ερυθρά Αιμοσφαίρια',
            'hgb' : 'HGB Αιμοσφαιρίνη',
            'hct' : 'HCT Αιματοκρίτης',
            'mcv' : 'MCV Μέσος Όγκος Ερυθρών',
            'mch' : 'MCH Μέση περιεκτικότης',
            'mchc': 'MCHC Μέση Συγκέντρωση',
            'rdw' : 'RDW Εύρος Κατανομής',
            'wbc' : 'WBC Λευκά Αιμοσφαίρια',
            'neu1' : 'NEU Ουδετερόφιλα %',
            'lym1' : 'LYM Λεμφοκύτταρα %',
            'mon1' : 'MON Μεγάλα μονοπύρηνα %',
            'eos1' : 'EOS Ηωσινόφιλα %',
            'baso1': 'BASO Βασεόφιλα %',
            'neu2' : 'NEU Ουδετερόφιλα #',
            'lym2' : 'LYM Λεμφοκύτταρα #',
            'mon2' : 'MON Μεγάλα μονοπύρηνα #',
            'eos2' : 'EOS Ηωσινόφιλα #',
            'baso2': 'BASO Βασεόφιλα #',
            'plt' : 'PLT Αιμοπετάλια',
            'pct' : 'PCT Αιμοπεταλιοκρίτης',
            'mpv' : 'MPV Μέσος όγκος αιμοπεταλίων',
            'pdw' : 'PDW Εύρος Κατανομής-PLT',

            # for df_medory_blood_biochemical_tests_table
            'glu' : 'Σάκχαρο',
            'ure' : 'Ουρία',
            'cre' : 'Κρεατινίνη',
            'urca' : 'Ουρικό οξύ',
            'hdl' : 'Χοληστερόλη ολική',
            'tri' : 'Τριγλυκερίδια',
            'sgot' : 'Οξαλοξεική τρανσαμινάση (SGOT)',
            'sgpt' : 'Πυροσταφυλική τρανσαμινάση (SGPT)',
            'ygt' : 'y-Γλουταμινική τρασφεράση',
            'na' : 'Νάτριο',
            'k' : 'Κάλιο',
            'ca' : 'Ασβέστιο ολικό',
            'fe' : 'Σίδηρος',
            'fer' : 'Φερριτίνη',

            # for medory_hematological_tests_table
            'tke' : 'Ταχύτητα καθίζησης ερυθρών',
            'b12' : 'Βιταμίνη Β12',

            # for medory_drug_levels_tests_table
            'ctni' : 'Τροπονίνη I (cTnI)'
        }
        for col in df.columns:
            for key in dict_columns_names:
                if key == col:
                    df.rename(columns = {col : dict_columns_names[key]}, inplace = True) 
        df['date']= pd.to_datetime(df['date'])
        df = df.drop(['id', 'created_at', 'user_id'], axis=1)
        df.sort_values(by='date', inplace = True)
        return df
#-----------------------------------End of Fetch all data from database for assigned user -------------------------------------#


#-----------------------------------Create the Sidebar Options -------------------------------------#
def display_sidebar(df):
    st.sidebar.write("Επιλέξτε το χρονικό διάστημα για προβολή αποτελεσμάτων:")
    start_date = pd.Timestamp(st.sidebar.date_input("Αρχική Ημερομηνία", df['date'].min().date()))
    end_date = pd.Timestamp(st.sidebar.date_input("Τελική Ημερομηνία", df['date'].max().date()))
    df = df.drop('date', axis=1)
    options_indicators =[" "] + [df.columns[i] for i in range (0, len(df.columns)) ]
    select_indicator = st.sidebar.selectbox("Επιλέξτε Δείκτη:", options = options_indicators)
    return select_indicator, start_date, end_date

#-----------------------------------End of Create the Sidebar Options -------------------------------------#

#-----------------------------------Create the Limits-------------------------------------#
def find_values_out_of_limit(df):
    df['Σάκχαρο'] = df['Σάκχαρο'].astype(float)
    df['Ουρία'] = df['Ουρία'].astype(float)
    df['Κρεατινίνη'] = df['Κρεατινίνη'].astype(float)
    df['Ουρικό οξύ'] = df['Ουρικό οξύ'].astype(float)
    df['Χοληστερόλη ολική'] = df['Χοληστερόλη ολική'].astype(float)
    
    for i in range(0,len(df)):
        count = 0
        if df['Σάκχαρο'][i] <= 70 or df['Σάκχαρο'][i] > 110 :
            count = count + 1 
            st.write("Ημερομηνία", df.date[i], ": Το σάκχαρο είναι εκτός ορίων.")
        if df['Ουρία'][i] < 15 or df['Ουρία'][i] > 50 :
            count = count + 1
            st.write("Ουρία", df.date[i], ": Η Ουρία είναι εκτός ορίων.")
        if df['Κρεατινίνη'][i] < 0.7 or df['Κρεατινίνη'][i] > 1.3:
            count = count + 1
            st.write("Ημερομηνία", df.date[i], ": Η Κρεατινίνη είναι εκτός ορίων.")
        if df['Ουρικό οξύ'][i] < 3 or df['Ουρικό οξύ'][i] > 7:
            count = count + 1
            st.write("Ημερομηνία", df.date[i], ": Το Ουρικό οξύ είναι εκτός ορίων  με τιμή", df['Ουρικό οξύ'][i], "και όρια x < 3 | x > 7" )
        if df['Χοληστερόλη ολική'][i] < 130 or df['Χοληστερόλη ολική'][i] > 220:
            count = count + 1
            st.write("Ημερομηνία", df.date[i], ": Η Χοληστερόλη ολική είναι εκτός ορίων  με τιμή", df['Χοληστερόλη ολική'][i], "και όρια x < 130 | x > 220" )
    if count == 0:
        st.write("Δεν υπάρχουν τιμές εκτός ορίων")
#-----------------------------------End of Create the Limits-------------------------------------#


#-----------------------------------Create the Charts-------------------------------------#
def display_charts(df, select_indicator, start_date, end_date):
    if select_indicator != ' ':
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        y_values = df[select_indicator][df["date"] >= start_date][df["date"] <= end_date]
         
        df = df.set_index('date')
        x_values = df.index.strftime("%d/%m/%Y")
        if len(y_values) >= 1:
            st.write("###### Προβολή αποτελεσμάτων για χρονικό διάστημα", start_date, " έως", end_date )
            fig = px.bar( x = x_values, y = y_values, 
                    title="Αποτελέσματα", width=900, height=500).update_traces(width = 0.1)
            fig.update_layout(margin=dict(l=20, r=220, t=50, b=20))
            fig.update_xaxes(rangemode='tozero', showgrid=False)
            fig.update_yaxes(rangemode='tozero', showgrid=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # fig1 = plt.figure(figsize=(8,7))
            # y_values.plot.bar()
            # plt.xlabel("Times of trial")
            # plt.ylabel(select_indicator)
            # st.pyplot(fig1)

        else:
            st.write("Δεν υπάρχουν εγγραφές για αυτό το διάστημα.")
    return
#-----------------------------------End of Create the Charts-------------------------------------#

def main():
    st.write("#### Προβολή αποτελεσμάτων εξετάσεων")
    row_index = select_all_from_medory_user_table()
    if row_index[0] >= 1:
        df = select_all_from_medory_blood_test_table(row_index)
        df
        select_indicator, start_date, end_date = display_sidebar(df)
        st.write("---")
        display_charts(df, select_indicator, start_date, end_date)
        check_out_of_limit_indicator = st.checkbox("Εμφάνισε τα αποτελέσματα εκτός ορίων")
        if check_out_of_limit_indicator:
            find_values_out_of_limit(df)
        


        
        
if __name__ == '__main__':
    main()
