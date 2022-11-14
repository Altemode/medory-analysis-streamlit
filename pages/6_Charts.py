import pandas as pd 
import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import gettext
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

            


