import pandas as pd 
import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Tefaa Metrics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Make the connection with Supabase - Database:
@st.experimental_singleton
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    #client = create_client(url, key)
    return create_client(url, key)
con = init_connection()

st.markdown("<h1 style='text-align: left; color: black; font-weight:900'>Στατιστικά Τιμών Εξετάσεων</h1>", unsafe_allow_html=True)

def select_all_from_medory_user_table():
    query=con.table("medory_user_table").select("*").execute()
    return query
query = select_all_from_medory_user_table()

df_medory_user_table = pd.DataFrame(query.data)

df_medory_user_table_unique_values = df_medory_user_table.copy()

assign_user = st.selectbox("Αναφορά Χρήστη  " , (df_medory_user_table_unique_values['fullname']))
row_index = df_medory_user_table_unique_values.index[df_medory_user_table_unique_values['fullname']==assign_user].tolist()

if assign_user != '':
    df_medory_user_table_unique_values['bmi'] = df_medory_user_table_unique_values['bmi'] = df_medory_user_table_unique_values['weight'] / ((df_medory_user_table_unique_values['height'] / 100) ** 2)
    st.sidebar.write("Όνομα:", df_medory_user_table_unique_values.loc[row_index[0]]['fullname'])
    st.sidebar.write("Ηλικία:", df_medory_user_table_unique_values.loc[row_index[0]]['age'])
    st.sidebar.write("Βάρος:", df_medory_user_table_unique_values.loc[row_index[0]]['weight'])
    st.sidebar.write("Ύψος:", df_medory_user_table_unique_values.loc[row_index[0]]['height'])
    st.sidebar.write("BMI:", round(df_medory_user_table_unique_values.loc[row_index[0]]['bmi'],3))

    st.markdown("<h1 style='text-align: left; color: black; font-weight:900'>Real-Time / Live Data Science Dashboard</h1>", unsafe_allow_html=True)

    select_tests = st.selectbox("Επίλεξε Εξέταση", options = ['', 'Γενική αίματος', 'Βιοχημικές'])

    if select_tests == 'Γενική αίματος':
        # Get data from medory_general_blood_tests_table:
            def select_all_from_medory_general_blood_tests_table():
                query=con.table("medory_general_blood_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_general_blood_tests_table()
            # Create dataframe with this data:
            df_medory_general_blood_tests_table = pd.DataFrame(query.data)
            # Set the columns names:
            if len(df_medory_general_blood_tests_table) > 0:
                df_medory_general_blood_tests_table.columns = ['ID', 'Created At', 'RBC Ερυθρά Αιμοσφαίρια', 'HGB Αιμοσφαιρίνη', 'HCT Αιματοκρίτης', 'MCV Μέσος Όγκος Ερυθρών', 'MCH Μέση περιεκτικότης', 
                                    'MCHC Μέση Συγκέντρωση', 'RDW Εύρος Κατανομής', 'WBC Λευκά Αιμοσφαίρια', 'NEU Ουδετερόφιλα %', 'LYM Λεμφοκύτταρα %', 
                                    'EOS Ηωσινόφιλα %', 'BASO Βασεόφιλα %', 'NEU Ουδετερόφιλα #', 'LYM Λεμφοκύτταρα #', 'MON Μεγάλα μονοπύρηνα #', 'EOS Ηωσινόφιλα #', 'BASO Βασεόφιλα #',
                                    'PLT Αιμοπετάλια', 'PCT Αιμοπεταλιοκρίτης', 'MPV Μέσος όγκος αιμοπεταλίων', 'PDW Εύρος Κατανομής-PLT', 'Αφορά Χρήστη']
                df_medory_general_blood_tests_table['Created At'] = pd.to_datetime(df_medory_general_blood_tests_table['Created At'])
                df_medory_general_blood_tests_table['Created At'] = df_medory_general_blood_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                df_medory_general_blood_tests_table['Year_Month'] = pd.to_datetime(df_medory_general_blood_tests_table['Created At'])
                df_medory_general_blood_tests_table['Year_Month'] = df_medory_general_blood_tests_table['Year_Month'].dt.strftime('%Y-%m')
                
                select_specific_test_value = st.selectbox( "Επίλεξε Συγκεκριμενη τιμή", options =[ '-', 'RBC Ερυθρά Αιμοσφαίρια', 'HGB Αιμοσφαιρίνη', 'HCT Αιματοκρίτης', 'MCV Μέσος Όγκος Ερυθρών', 'MCH Μέση περιεκτικότης', 
                                    'MCHC Μέση Συγκέντρωση', 'RDW Εύρος Κατανομής', 'WBC Λευκά Αιμοσφαίρια', 'NEU Ουδετερόφιλα %', 'LYM Λεμφοκύτταρα %', 
                                    'EOS Ηωσινόφιλα %', 'BASO Βασεόφιλα %', 'NEU Ουδετερόφιλα #', 'LYM Λεμφοκύτταρα #', 'MON Μεγάλα μονοπύρηνα #', 'EOS Ηωσινόφιλα #', 'BASO Βασεόφιλα #',
                                    'PLT Αιμοπετάλια', 'PCT Αιμοπεταλιοκρίτης', 'MPV Μέσος όγκος αιμοπεταλίων', 'PDW Εύρος Κατανομής-PLT'])

                if select_specific_test_value != '-':
                    choose_year_month = st.multiselect(label = 'Διάλεξε Έτη', options = pd.unique(df_medory_general_blood_tests_table["Year_Month"]))

                    if choose_year_month:
                        # Display the dataframe:
                        st.subheader("Γενική εξέταση αίματος για {}".format(assign_user))
                        df_medory_general_blood_tests_table = df_medory_general_blood_tests_table.loc[df_medory_general_blood_tests_table['Year_Month'].isin(choose_year_month)]
                    
                        st.write("Γράφημα για {} ".format(select_specific_test_value), 'για χρονιές και μήνα ', *choose_year_month)
                        fig3 = px.bar(data_frame=df_medory_general_blood_tests_table, x=choose_year_month, y=select_specific_test_value)
                        fig3.update_layout(
                            
                            margin=dict(l=0, r=20, t=10, b=60),
                            #paper_bgcolor="LightSteelBlue",
                        )
                        
                   
                        st.plotly_chart(fig3,use_container_width=True)
            else:
                st.write("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια")
            
    if select_tests == 'Βιοχημικές':
        # Get data from medory_blood_biochemical_tests_table:
            def select_all_from_medory_blood_biochemical_tests_table():
                query=con.table("medory_blood_biochemical_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_blood_biochemical_tests_table()
            # Create dataframe with this data:
            df_medory_blood_biochemical_tests_table = pd.DataFrame(query.data)
            # Set the columns names:
            if len(df_medory_blood_biochemical_tests_table) > 0:
                df_medory_blood_biochemical_tests_table.columns = ['ID', 'Created At', 'Σάκχαρο', 'Ουρία', 'Κρεατινίνη', 'Ουρικό οξύ', 'Χοληστερόλη ολική', 
                                    'Τριγλυκερίδια', 'Οξαλοξεική τρανσαμινάση (SGOT)', 'Πυροσταφυλική τρανσαμινάση (SGPT)', 'y-Γλουταμινική τρασφεράση', 'Νάτριο', 
                                    'Κάλιο', 'Ασβέστιο ολικό', 'Σίδηρος', 'Φερριτίνη', 'Αφορά Χρήστη']
                df_medory_blood_biochemical_tests_table['Created At'] = pd.to_datetime(df_medory_blood_biochemical_tests_table['Created At'])
                df_medory_blood_biochemical_tests_table['Created At'] = df_medory_blood_biochemical_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                df_medory_blood_biochemical_tests_table['Year'] = pd.to_datetime(df_medory_blood_biochemical_tests_table['Created At'])
                df_medory_blood_biochemical_tests_table['Year'] = df_medory_blood_biochemical_tests_table['Year'].dt.strftime('%Y')

                select_specific_test_value = st.selectbox( "Επίλεξε Συγκεκριμενη τιμή",  options =  ['-', 'Σάκχαρο', 'Ουρία', 'Κρεατινίνη', 'Ουρικό οξύ', 'Χοληστερόλη ολική', 
                                    'Τριγλυκερίδια', 'Οξαλοξεική τρανσαμινάση (SGOT)', 'Πυροσταφυλική τρανσαμινάση (SGPT)', 'y-Γλουταμινική τρασφεράση', 'Νάτριο', 
                                    'Κάλιο', 'Ασβέστιο ολικό', 'Σίδηρος', 'Φερριτίνη'])



                choose_year = st.multiselect(label = 'Διάλεξε Έτη', options = df_medory_blood_biochemical_tests_table['Year'])
                if choose_year:
                    # Display the dataframe:
                    st.subheader("Γενική εξέταση αίματος για {}".format(assign_user))
                    df_medory_blood_biochemical_tests_table = df_medory_blood_biochemical_tests_table.loc[df_medory_blood_biochemical_tests_table['Year'].isin(choose_year)]
                
                    st.markdown("<h5 style='text-align: center; padding-top: 15px; color: Darkblue; font-weight:900'>Counts Per Age.</h1>", unsafe_allow_html=True)
                    #st.markdown("### Counts Per Age!")
                    fig3 = px.bar(data_frame=df_medory_blood_biochemical_tests_table, x=select_specific_test_value)
                    fig3.update_layout(
                        margin=dict(l=0, r=20, t=10, b=60),
                        #paper_bgcolor="LightSteelBlue",
                        
                        
                    )
                    

                    st.plotly_chart(fig3,use_container_width=True)


            else:
                st.write("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια")
            

            


