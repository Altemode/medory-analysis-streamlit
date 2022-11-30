import pandas as pd 
import numpy as np
import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import gettext
import functools as ft
from functools import reduce
_ = gettext.gettext

st.set_page_config(
    page_title="Tefaa Metrics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Menu switcher for the languages:
language = st.sidebar.selectbox(_('Επίλεξε Γλώσσα'), ['eng', 'gr'])
try:
  localizator = gettext.translation('base', localedir='locales', languages=[language])
  localizator.install()
  _ = localizator.gettext 
except:
    pass


#Make the connection with Supabase - Database:
@st.experimental_singleton
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    #client = create_client(url, key)
    return create_client(url, key)
con = init_connection()

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


st.markdown("Στατιστικά Τιμών Εξετάσεων")

#--------------------------------Fetch all users from database and assign user--------------------------------#

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

#-----------------------------------End of Fetch all users from database -------------------------------------#

    
    #---------- FETCH DATA FROM ALL TABLES ---------------#
    dfs=[]
    #### 1 Fetch all data from medory_general_blood_tests_table:
    def select_all_from_medory_general_blood_tests_table():
        query=con.table("medory_general_blood_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
        return query
    query = select_all_from_medory_general_blood_tests_table()
    df_medory_general_blood_tests_table = pd.DataFrame(query.data)
    # Exclude some unnecessary columns:
    df_medory_general_blood_tests_table = df_medory_general_blood_tests_table.loc[:, ~df_medory_general_blood_tests_table.columns.isin(['id', 'user_id'])]
    if len(df_medory_general_blood_tests_table) > 0:
        dfs.append(df_medory_general_blood_tests_table)

    #### 2 Fetch all data from medory_blood_biochemical_tests_table:
    def select_all_from_medory_blood_biochemical_tests_table():
        query=con.table("medory_blood_biochemical_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
        return query
    query = select_all_from_medory_blood_biochemical_tests_table()
    df_medory_blood_biochemical_tests_table = pd.DataFrame(query.data)
    # Exclude some unnecessary columns:
    df_medory_blood_biochemical_tests_table = df_medory_blood_biochemical_tests_table.loc[:, ~df_medory_blood_biochemical_tests_table.columns.isin(['id', 'user_id'])]
    if len(df_medory_blood_biochemical_tests_table) > 0:
        dfs.append(df_medory_blood_biochemical_tests_table)

    #### 3 Fetch all data from medory_hematological_tests_table:
    def select_all_from_medory_hematological_tests_table():
        query=con.table("medory_hematological_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
        return query
    query = select_all_from_medory_hematological_tests_table()
    df_medory_hematological_tests_table = pd.DataFrame(query.data)
    # Exclude some unnecessary columns:
    df_medory_hematological_tests_table = df_medory_hematological_tests_table.loc[:, ~df_medory_hematological_tests_table.columns.isin(['id', 'user_id'])]
    if len(df_medory_hematological_tests_table) > 0:
        dfs.append(df_medory_hematological_tests_table)

    #### 4 Fetch all data from medory_drug_levels_tests_table:
    def select_all_from_medory_drug_levels_tests_table():
        query=con.table("medory_drug_levels_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
        return query
    query = select_all_from_medory_drug_levels_tests_table()
    df_medory_drug_levels_tests_table = pd.DataFrame(query.data)
    # Exclude some unnecessary columns:
    df_medory_drug_levels_tests_table = df_medory_drug_levels_tests_table.loc[:, ~df_medory_drug_levels_tests_table.columns.isin(['id', 'user_id'])]  
    if len(df_medory_drug_levels_tests_table) > 0:
        dfs.append(df_medory_drug_levels_tests_table)
    
    #---------- End of FETCH DATA FROM ALL TABLES ---------------#


    #-----------Merge & processing this Dataframe -------------#

    if len(dfs) > 0:

        #merge all DataFrames into one
        df_merged = reduce(lambda  left, right: pd.merge(left, right, on=['created_at'], how='outer'), dfs)

        # Second i create a new column with Date name, that includes Year, Month, Day from Column Created At:
        df_merged['created_at'] = pd.to_datetime(df_merged['created_at'])
        df_merged['Date'] = df_merged['created_at'].dt.strftime('%Y-%m-%d')
        df_merged["-"] = np.nan
        # Third exclude created_at column:
        df_merged = df_merged.loc[:, ~df_merged.columns.isin(['created_at'])]

        # Set Columns name for df_merged:
        for col in df_merged.columns:
            for key in dict_columns_names:
                if key == col:
                    df_merged.rename(columns = {col : dict_columns_names[key]}, inplace = True)     
    
        # shift column '-' to first position
        first_column = df_merged.pop('-')
        # insert column using insert(position,column_name, first_column) function
        df_merged.insert(0, '-', first_column)

        # Set index
        df_merged.set_index(('Date'), inplace=True)
        # Set index name
        df_merged.index.name='Dates'
        # Fourth sorting datatable:
        df_merged.sort_index( ascending = False, inplace=True)
    
        #-----------End of Merge & processing this Dataframe -------------#


        #-----------Create Chart depending on selected indicator and dates -------------#
        select_specific_indicator = st.selectbox(_(''), options = df_merged.columns )

        # Drop rows with <NA> values:
        df_merged.dropna(subset=[select_specific_indicator], inplace=True)

        if select_specific_indicator != '-':
            choose_date = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_merged.index)
            if choose_date:
                # Display the dataframe:
                df_merged = df_merged.loc[df_merged.index.isin(choose_date)]
                
                
                #Create the chart;
                fig3 = px.bar(data_frame=df_merged, x=choose_date,  y=select_specific_indicator)
                fig3.update_layout(
                    margin=dict(l=0, r=20, t=0, b=60),
                )
                st.write("---")
                col1,col2 = st.columns([2,1], gap='medium')
                with col1:
                    st.write(_("**Γράφημα για {}**").format(select_specific_indicator))
                    st.plotly_chart(fig3, use_container_width=True)
                with col2:
                    st.write(_("**Τιμές για {}**").format(select_specific_indicator))
                    st.dataframe(df_merged[select_specific_indicator], use_container_width=True)

        else:
            st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

        #-----------End of Create Chart depending on selected indicator and dates -------------#


    else: 
        st.write(_("**Δεν υπάρχουν εγγραφές για το άτομο {}**".format(assign_user)))

    

    st.write('---')

    select_tests = st.selectbox(_("Επίλεξε Εξέταση"), options = ['', _("Γενική αίματος"), _("Βιοχημικές"), _("Αιματολογικές"), _('Επίπεδα Φαρμάκων'), _('Έλεγχος Θυρεοειδούς'), _('Ορολογικές'), _('Βιταμίνες')])

    if select_tests == _('Γενική αίματος'):
        # Get data from medory_general_blood_tests_table:
            def select_all_from_medory_general_blood_tests_table():
                query=con.table("medory_general_blood_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_general_blood_tests_table()
            # Create dataframe with this data:
            df_medory_general_blood_tests_table = pd.DataFrame(query.data)
            # Set the columns names:
            if len(df_medory_general_blood_tests_table) > 0:
                df_medory_general_blood_tests_table.columns = ['ID', 'Created At', _('RBC Ερυθρά Αιμοσφαίρια'), _('HGB Αιμοσφαιρίνη'), _('HCT Αιματοκρίτης'), _('MCV Μέσος Όγκος Ερυθρών'), _('MCH Μέση περιεκτικότης'), 
                            _('MCHC Μέση Συγκέντρωση'), _('RDW Εύρος Κατανομής'), _('WBC Λευκά Αιμοσφαίρια'), _('NEU Ουδετερόφιλα %'), _('LYM Λεμφοκύτταρα %'), 
                            _('EOS Ηωσινόφιλα %'), _('BASO Βασεόφιλα %'), _('NEU Ουδετερόφιλα #'), _('LYM Λεμφοκύτταρα #'), _('MON Μεγάλα μονοπύρηνα #'), _('EOS Ηωσινόφιλα #'), _('BASO Βασεόφιλα #'),
                            _('PLT Αιμοπετάλια'), _('PCT Αιμοπεταλιοκρίτης'), _('MPV Μέσος όγκος αιμοπεταλίων'), _('PDW Εύρος Κατανομής-PLT'), _('Αφορά Χρήστη')]
                df_medory_general_blood_tests_table['Created At'] = pd.to_datetime(df_medory_general_blood_tests_table['Created At'])
                df_medory_general_blood_tests_table['Created At'] = df_medory_general_blood_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                df_medory_general_blood_tests_table['Year_Month'] = pd.to_datetime(df_medory_general_blood_tests_table['Created At'])
                df_medory_general_blood_tests_table['Year_Month'] = df_medory_general_blood_tests_table['Year_Month'].dt.strftime('%Y-%m')
                df_medory_general_blood_tests_table.sort_values(by='Year_Month', ascending = False, inplace=True)

                select_specific_test_value = st.selectbox( _("Επίλεξε Συγκεκριμενη τιμή"), options =[ '-',  _('RBC Ερυθρά Αιμοσφαίρια'), _('HGB Αιμοσφαιρίνη'), _('HCT Αιματοκρίτης'), _('MCV Μέσος Όγκος Ερυθρών'), _('MCH Μέση περιεκτικότης'), 
                            _('MCHC Μέση Συγκέντρωση'), _('RDW Εύρος Κατανομής'), _('WBC Λευκά Αιμοσφαίρια'), _('NEU Ουδετερόφιλα %'), _('LYM Λεμφοκύτταρα %'), 
                            _('EOS Ηωσινόφιλα %'), _('BASO Βασεόφιλα %'), _('NEU Ουδετερόφιλα #'), _('LYM Λεμφοκύτταρα #'), _('MON Μεγάλα μονοπύρηνα #'), _('EOS Ηωσινόφιλα #'), _('BASO Βασεόφιλα #'),
                            _('PLT Αιμοπετάλια'), _('PCT Αιμοπεταλιοκρίτης'), _('MPV Μέσος όγκος αιμοπεταλίων'), _('PDW Εύρος Κατανομής-PLT')])

                if select_specific_test_value != '-':
                    choose_year_month = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = pd.unique(df_medory_general_blood_tests_table["Year_Month"]))

                    if choose_year_month:
                        # Display the dataframe:
                        df_medory_general_blood_tests_table = df_medory_general_blood_tests_table.loc[df_medory_general_blood_tests_table['Year_Month'].isin(choose_year_month)]
                        st.subheader(_("{} - Γράφημα για {}").format(select_tests, select_specific_test_value))
                        #Create the chart;
                        fig3 = px.bar(data_frame=df_medory_general_blood_tests_table, x=choose_year_month, y=select_specific_test_value)
                        fig3.update_layout(
                            margin=dict(l=0, r=20, t=10, b=60),
                        )
                        st.plotly_chart(fig3,use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))
            
    if select_tests == _('Βιοχημικές'):
        # Get data from medory_blood_biochemical_tests_table:
            def select_all_from_medory_blood_biochemical_tests_table():
                query=con.table("medory_blood_biochemical_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_blood_biochemical_tests_table()
            # Create dataframe with this data:
            df_medory_blood_biochemical_tests_table = pd.DataFrame(query.data)
            # Set the columns names:
            if len(df_medory_blood_biochemical_tests_table) > 0:
                df_medory_blood_biochemical_tests_table.columns = ['ID', 'Created At', _('Σάκχαρο'), _('Ουρία'), _('Κρεατινίνη'), _('Ουρικό οξύ'), _('Χοληστερόλη ολική'), 
                                    _('Τριγλυκερίδια'), _('Οξαλοξεική τρανσαμινάση (SGOT)'), _('Πυροσταφυλική τρανσαμινάση (SGPT)'), _('y-Γλουταμινική τρασφεράση'), _('Νάτριο'), 
                                    _('Κάλιο'), _('Ασβέστιο ολικό'), _('Σίδηρος'), _('Φερριτίνη'), _('Αφορά Χρήστη')]
                df_medory_blood_biochemical_tests_table['Created At'] = pd.to_datetime(df_medory_blood_biochemical_tests_table['Created At'])
                df_medory_blood_biochemical_tests_table['Created At'] = df_medory_blood_biochemical_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                df_medory_blood_biochemical_tests_table['Year_Month'] = pd.to_datetime(df_medory_blood_biochemical_tests_table['Created At'])
                df_medory_blood_biochemical_tests_table['Year_Month'] = df_medory_blood_biochemical_tests_table['Year_Month'].dt.strftime('%Y-%m')
                df_medory_blood_biochemical_tests_table.sort_values(by='Year_Month', ascending = False, inplace=True)


                select_specific_test_value = st.selectbox( _("Επίλεξε Συγκεκριμενη τιμή"),  options =  ['-', _('Σάκχαρο'), _('Ουρία'), _('Κρεατινίνη'), _('Ουρικό οξύ'), _('Χοληστερόλη ολική'), 
                                    _('Τριγλυκερίδια'), _('Οξαλοξεική τρανσαμινάση (SGOT)'), _('Πυροσταφυλική τρανσαμινάση (SGPT)'), _('y-Γλουταμινική τρασφεράση'), _('Νάτριο'), 
                                    _('Κάλιο'), _('Ασβέστιο ολικό'), _('Σίδηρος'), _('Φερριτίνη')])

                if select_specific_test_value != '-':
                    choose_year_month = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_blood_biochemical_tests_table['Year_Month'])
                    if choose_year_month:
                        # Display the dataframe:
                        df_medory_blood_biochemical_tests_table = df_medory_blood_biochemical_tests_table.loc[df_medory_blood_biochemical_tests_table['Year_Month'].isin(choose_year_month)]
                        st.subheader(_("{} - Γράφημα για {}").format(select_tests, select_specific_test_value))
                        #st.markdown("### Counts Per Age!")
                        fig3 = px.bar(data_frame=df_medory_blood_biochemical_tests_table, x=choose_year_month, y=select_specific_test_value)
                        fig3.update_layout(
                            margin=dict(l=0, r=20, t=10, b=60),
                            #paper_bgcolor="LightSteelBlue",   
                        )

                        st.plotly_chart(fig3,use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))
    

    if select_tests == _('Αιματολογικές'):
        # Get data from medory_hematological_tests_table:
            def select_all_from_medory_hematological_tests_table():
                query=con.table("medory_hematological_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_hematological_tests_table()
            # Create dataframe with this data:
            df_medory_hematological_tests_table = pd.DataFrame(query.data)
            # Set the columns names:
            if len(df_medory_hematological_tests_table) > 0:
                df_medory_hematological_tests_table.columns = ['ID', 'Created At', _('Ταχύτητα καθίζησης ερυθρών'), _('Βιταμίνη Β12'), _('Αφορά Χρήστη')]
                df_medory_hematological_tests_table['Created At'] = pd.to_datetime(df_medory_hematological_tests_table['Created At'])
                df_medory_hematological_tests_table['Created At'] = df_medory_hematological_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                df_medory_hematological_tests_table['Year_Month'] = pd.to_datetime(df_medory_hematological_tests_table['Created At'])
                df_medory_hematological_tests_table['Year_Month'] = df_medory_hematological_tests_table['Year_Month'].dt.strftime('%Y-%m')
                df_medory_hematological_tests_table.sort_values(by='Year_Month', ascending = False, inplace=True)


                select_specific_test_value = st.selectbox( _("Επίλεξε Συγκεκριμενη τιμή"),  options =  ['-', _('Ταχύτητα καθίζησης ερυθρών'), _('Βιταμίνη Β12')])
                if select_specific_test_value != '-':
                    choose_year_month = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_hematological_tests_table['Year_Month'])
                    if choose_year_month:
                        # Display the dataframe:
                        df_medory_hematological_tests_table = df_medory_hematological_tests_table.loc[df_medory_hematological_tests_table['Year_Month'].isin(choose_year_month)]
                        st.subheader(_("{} - Γράφημα για {}").format(select_tests, select_specific_test_value))
                        #st.markdown("### Counts Per Age!")
                        fig3 = px.bar(data_frame=df_medory_hematological_tests_table, x=choose_year_month, y=select_specific_test_value)
                        fig3.update_layout(
                            margin=dict(l=0, r=20, t=10, b=60),
                            #paper_bgcolor="LightSteelBlue",   
                        )
                        st.plotly_chart(fig3,use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

    if select_tests == _('Επίπεδα Φαρμάκων'):
        # Get data from medory_drug_levels_tests_table:
            def select_all_from_medory_drug_levels_tests_table():
                query=con.table("medory_drug_levels_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_drug_levels_tests_table()
            # Create dataframe with this data:
            df_medory_drug_levels_tests_table = pd.DataFrame(query.data)
            # Set the columns names:
            if len(df_medory_drug_levels_tests_table) > 0:
                df_medory_drug_levels_tests_table.columns = ['ID', 'Created At', _("Τροπονίνη Ι (cTnI)"), _('Αφορά Χρήστη')]
                df_medory_drug_levels_tests_table['Created At'] = pd.to_datetime(df_medory_drug_levels_tests_table['Created At'])
                df_medory_drug_levels_tests_table['Created At'] = df_medory_drug_levels_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                df_medory_drug_levels_tests_table['Year_Month'] = pd.to_datetime(df_medory_drug_levels_tests_table['Created At'])
                df_medory_drug_levels_tests_table['Year_Month'] = df_medory_drug_levels_tests_table['Year_Month'].dt.strftime('%Y-%m')
                df_medory_drug_levels_tests_table.sort_values(by='Year_Month', ascending = False, inplace=True)


                select_specific_test_value = st.selectbox( _("Επίλεξε Συγκεκριμενη τιμή"),  options =  ['-', _("Τροπονίνη Ι (cTnI)")])
                if select_specific_test_value != '-':
                    choose_year_month = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_drug_levels_tests_table['Year_Month'])
                    if choose_year_month:
                        # Display the dataframe:
                        df_medory_drug_levels_tests_table = df_medory_drug_levels_tests_table.loc[df_medory_drug_levels_tests_table['Year_Month'].isin(choose_year_month)]
                        st.subheader(_("{} - Γράφημα για {}").format(select_tests, select_specific_test_value))
                        #st.markdown("### Counts Per Age!")
                        fig3 = px.bar(data_frame=df_medory_drug_levels_tests_table, x=choose_year_month, y=select_specific_test_value)
                        fig3.update_layout(
                            margin=dict(l=0, r=20, t=10, b=60),
                            #paper_bgcolor="LightSteelBlue",   
                        )
                        st.plotly_chart(fig3,use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

    if select_tests == _('Έλεγχος Θυρεοειδούς'):
        # Get data from medory_thyroid_check_tests_table:
            def select_all_from_medory_thyroid_check_tests_table():
                query=con.table("medory_thyroid_check_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_thyroid_check_tests_table()
            # Create dataframe with this data:
            df_medory_thyroid_check_tests_table = pd.DataFrame(query.data)
            # Set the columns names:
            if len(df_medory_thyroid_check_tests_table) > 0:
                df_medory_thyroid_check_tests_table.columns = ['ID', 'Created At', _("Θυρεοτρόπος ορμονη TSH"), _('Αφορά Χρήστη')]
                df_medory_thyroid_check_tests_table['Created At'] = pd.to_datetime(df_medory_thyroid_check_tests_table['Created At'])
                df_medory_thyroid_check_tests_table['Created At'] = df_medory_thyroid_check_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                df_medory_thyroid_check_tests_table['Year_Month'] = pd.to_datetime(df_medory_thyroid_check_tests_table['Created At'])
                df_medory_thyroid_check_tests_table['Year_Month'] = df_medory_thyroid_check_tests_table['Year_Month'].dt.strftime('%Y-%m')
                df_medory_thyroid_check_tests_table.sort_values(by='Year_Month', ascending = False, inplace=True)


                select_specific_test_value = st.selectbox( _("Επίλεξε Συγκεκριμενη τιμή"),  options =  ['-', _("Θυρεοτρόπος ορμονη TSH")])
                if select_specific_test_value != '-':
                    choose_year_month = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_thyroid_check_tests_table['Year_Month'])
                    if choose_year_month:
                        # Display the dataframe:
                        df_medory_thyroid_check_tests_table = df_medory_thyroid_check_tests_table.loc[df_medory_thyroid_check_tests_table['Year_Month'].isin(choose_year_month)]
                        st.subheader(_("{} - Γράφημα για {}").format(select_tests, select_specific_test_value))
                        #st.markdown("### Counts Per Age!")
                        fig3 = px.bar(data_frame=df_medory_thyroid_check_tests_table, x=choose_year_month, y=select_specific_test_value)
                        fig3.update_layout(
                            margin=dict(l=0, r=20, t=10, b=60),
                            #paper_bgcolor="LightSteelBlue",   
                        )
                        st.plotly_chart(fig3,use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))
        

    if select_tests == _('Ορολογικές'):
        # Get data from medory_serological_tests_table:
            def select_all_from_medory_serological_tests_table():
                query=con.table("medory_serological_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_serological_tests_table()
            # Create dataframe with this data:
            df_medory_serological_tests_table = pd.DataFrame(query.data)
            # Set the columns names:
            if len(df_medory_serological_tests_table) > 0:
                df_medory_serological_tests_table.columns = ['ID', 'Created At', _("C-αντιδρώσα (ποσοτική) πρωτείνη (CRP)"), _('Αφορά Χρήστη')]
                df_medory_serological_tests_table['Created At'] = pd.to_datetime(df_medory_serological_tests_table['Created At'])
                df_medory_serological_tests_table['Created At'] = df_medory_serological_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                df_medory_serological_tests_table['Year_Month'] = pd.to_datetime(df_medory_serological_tests_table['Created At'])
                df_medory_serological_tests_table['Year_Month'] = df_medory_serological_tests_table['Year_Month'].dt.strftime('%Y-%m')
                df_medory_serological_tests_table.sort_values(by='Year_Month', ascending = False, inplace=True)


                select_specific_test_value = st.selectbox( _("Επίλεξε Συγκεκριμενη τιμή"),  options =  ['-', _("C-αντιδρώσα (ποσοτική) πρωτείνη (CRP)")])
                if select_specific_test_value != '-':
                    choose_year_month = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_serological_tests_table['Year_Month'])
                    if choose_year_month:
                        # Display the dataframe:
                        df_medory_serological_tests_table = df_medory_serological_tests_table.loc[df_medory_serological_tests_table['Year_Month'].isin(choose_year_month)]
                        st.subheader(_("{} - Γράφημα για {}").format(select_tests, select_specific_test_value))
                        #st.markdown("### Counts Per Age!")
                        fig3 = px.bar(data_frame=df_medory_serological_tests_table, x=choose_year_month, y=select_specific_test_value)
                        fig3.update_layout(
                            margin=dict(l=0, r=20, t=10, b=60),
                            #paper_bgcolor="LightSteelBlue",   
                        )
                        st.plotly_chart(fig3,use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))
            

    if select_tests == _('Βιταμίνες'):
        # Get data from medory_vitamins_tests_table:
            def select_all_from_medory_vitamins_tests_table():
                query=con.table("medory_vitamins_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_vitamins_tests_table()
            # Create dataframe with this data:
            df_medory_vitamins_tests_table = pd.DataFrame(query.data)
            # Set the columns names:
            if len(df_medory_vitamins_tests_table) > 0:
                df_medory_vitamins_tests_table.columns = ['ID', 'Created At', _("Βιταμίνη 25OH D3"), _('Αφορά Χρήστη')]
                df_medory_vitamins_tests_table['Created At'] = pd.to_datetime(df_medory_vitamins_tests_table['Created At'])
                df_medory_vitamins_tests_table['Created At'] = df_medory_vitamins_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                df_medory_vitamins_tests_table['Year_Month'] = pd.to_datetime(df_medory_vitamins_tests_table['Created At'])
                df_medory_vitamins_tests_table['Year_Month'] = df_medory_vitamins_tests_table['Year_Month'].dt.strftime('%Y-%m')
                df_medory_vitamins_tests_table.sort_values(by='Year_Month', ascending = False, inplace=True)


                select_specific_test_value = st.selectbox( _("Επίλεξε Συγκεκριμενη τιμή"),  options =  ['-', _("Βιταμίνη 25OH D3")])
                if select_specific_test_value != '-':
                    choose_year_month = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_vitamins_tests_table['Year_Month'])
                    if choose_year_month:
                        # Display the dataframe:
                        df_medory_vitamins_tests_table = df_medory_vitamins_tests_table.loc[df_medory_vitamins_tests_table['Year_Month'].isin(choose_year_month)]
                        st.subheader(_("{} - Γράφημα για {}").format(select_tests, select_specific_test_value))
                        #st.markdown("### Counts Per Age!")
                        fig3 = px.bar(data_frame=df_medory_vitamins_tests_table, x=choose_year_month, y=select_specific_test_value)
                        fig3.update_layout(
                            margin=dict(l=0, r=20, t=10, b=60),
                            #paper_bgcolor="LightSteelBlue",   
                        )
                        st.plotly_chart(fig3,use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

            


