import pandas as pd 
import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import datetime
import gettext
_ = gettext.gettext


st.set_page_config(
    page_title="Tefaa Metrics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

language = st.sidebar.selectbox('', ['eng', 'gr'])
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

def select_all_from_medory_user_table():
    query=con.table("medory_user_table").select("*").execute()
    return query
query = select_all_from_medory_user_table()

df_medory_user_table = pd.DataFrame(query.data)

df_medory_user_table_unique_values = df_medory_user_table.copy()
st.title(_("Αποτελέσματα Τιμών Εξετάσεων Αίματος"))


assign_user = st.selectbox(_("Αναφορά Χρήστη ") , (df_medory_user_table_unique_values['fullname']))
row_index = df_medory_user_table_unique_values.index[df_medory_user_table_unique_values['fullname']==assign_user].tolist()


if assign_user != '':
    st.sidebar.markdown(_("## Έχεις επιλέξει τον παρακάτω χρήστη."))

    df_medory_user_table_unique_values['bmi'] = df_medory_user_table_unique_values['weight'] / ((df_medory_user_table_unique_values['height'] / 100) ** 2)
    st.sidebar.write(_("Όνομα:"), df_medory_user_table_unique_values.loc[row_index[0]]['fullname'])
    st.sidebar.write(_("Ηλικία:"), df_medory_user_table_unique_values.loc[row_index[0]]['age'])
    st.sidebar.write(_("Βάρος:"), df_medory_user_table_unique_values.loc[row_index[0]]['weight'])
    st.sidebar.write(_("Ύψος:"), df_medory_user_table_unique_values.loc[row_index[0]]['height'])
    st.sidebar.write(_("BMI:"), round(df_medory_user_table_unique_values.loc[row_index[0]]['bmi'],3))

    with st.expander(_("Πατείστε για άνοιγμα/κλείσιμο"), expanded = True):
        st.subheader(_("Επίλεξε είδος εξέτασης για τον {}").format(assign_user))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            check1 = st.checkbox(_("Γενική εξέταση αίματος"))
            check2 = st.checkbox(_("Βιοχημικές"))
            check3 = st.checkbox(_("Αιματολογικές Εξετάσεις"))
            check4 = st.checkbox(_("Επίπεδα Φαρμάκων"))
            check5 = st.checkbox(_("Έλεγχος Θυροειδούς"))
            check6 = st.checkbox(_("Ορολογικές"))
        with col2:
            check7 = st.checkbox("other1")
            check8 = st.checkbox("other2")
            check9 = st.checkbox("other3")
            check10 = st.checkbox("other4")
            check11 = st.checkbox("other5")
            check12 = st.checkbox("other6")
        with col3:
            check13 = st.checkbox("other7")
            check14 = st.checkbox("other8")
            check15 = st.checkbox("other9")
            check16 = st.checkbox("other10")
            check17 = st.checkbox("other11")
            check18 = st.checkbox("other12")
        
        with col4:
            check19 = st.checkbox("other13")
            check20 = st.checkbox("other14")
            check21 = st.checkbox("other15")
            check22 = st.checkbox("other16")
            check23 = st.checkbox("other17")
            check24 = st.checkbox("other18")

    st.markdown("""---""")

    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        # For General Blood Tests
        if check1:
            # Get data from medory_general_blood_tests_table:
            def select_all_from_medory_general_blood_tests_table():
                query=con.table("medory_general_blood_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_general_blood_tests_table()
            # Create dataframe with this data:
            df_medory_general_blood_tests_table = pd.DataFrame(query.data)
            if len(df_medory_general_blood_tests_table) > 0:
                # Set the columns names:
                df_medory_general_blood_tests_table.columns = ['ID', 'Created At', _('RBC Ερυθρά Αιμοσφαίρια'), _('HGB Αιμοσφαιρίνη'), _('HCT Αιματοκρίτης'), _('MCV Μέσος Όγκος Ερυθρών'), _('MCH Μέση περιεκτικότης'), 
                            _('MCHC Μέση Συγκέντρωση'), _('RDW Εύρος Κατανομής'), _('WBC Λευκά Αιμοσφαίρια'), _('NEU Ουδετερόφιλα %'), _('LYM Λεμφοκύτταρα %'), 
                            _('EOS Ηωσινόφιλα %'), _('BASO Βασεόφιλα %'), _('NEU Ουδετερόφιλα #'), _('LYM Λεμφοκύτταρα #'), _('MON Μεγάλα μονοπύρηνα #'), _('EOS Ηωσινόφιλα #'), _('BASO Βασεόφιλα #'),
                            _('PLT Αιμοπετάλια'), _('PCT Αιμοπεταλιοκρίτης'), _('MPV Μέσος όγκος αιμοπεταλίων'), _('PDW Εύρος Κατανομής-PLT'), _('Αφορά Χρήστη')]
                # Set the Create At column to be datetime column:
                df_medory_general_blood_tests_table['Created At'] = pd.to_datetime(df_medory_general_blood_tests_table['Created At'])
                # Edit this column to keep only year, month and day:
                df_medory_general_blood_tests_table['Created At'] = df_medory_general_blood_tests_table['Created At'].dt.strftime('%Y-%m-%d')
                # Create new Year column and set this as datetime column:
                df_medory_general_blood_tests_table['Year'] = pd.to_datetime(df_medory_general_blood_tests_table['Created At'])
                # Edit this Year column to keep only data of Year. We need this to select Year below:
                df_medory_general_blood_tests_table['Year'] = df_medory_general_blood_tests_table['Year'].dt.strftime('%Y')
                # Choose year to display results based on it:
                choose_year = st.multiselect(label = _('Διάλεξε Έτη'), options = df_medory_general_blood_tests_table['Year'])
                if choose_year:
                    # Display the dataframe:
                    st.subheader(_("Γενική εξέταση αίματος για {}").format(assign_user))
                    # Edit dataframe to keep data depending on above choose year:
                    df_medory_general_blood_tests_table = df_medory_general_blood_tests_table.loc[df_medory_general_blood_tests_table['Year'].isin(choose_year)]
                    # Display dataframe all columns, exclude specidic:
                    st.dataframe(df_medory_general_blood_tests_table.loc[:, ~df_medory_general_blood_tests_table.columns.isin(['Year', 'ID', 'Αφορά Χρήστη'])].T, height = 800, use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

    with col2:
        # For Biochemical Tests:
        if check2:
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
                df_medory_blood_biochemical_tests_table['Year'] = pd.to_datetime(df_medory_blood_biochemical_tests_table['Created At'])
                df_medory_blood_biochemical_tests_table['Year'] = df_medory_blood_biochemical_tests_table['Year'].dt.strftime('%Y')

                choose_year = st.multiselect(label = _('Διάλεξε Έτη'), options = df_medory_blood_biochemical_tests_table['Year'])
                if choose_year:

                    # Display the dataframe:
                    st.subheader(_("Βιοχημικές Αίματος"))
                    df_medory_blood_biochemical_tests_table = df_medory_blood_biochemical_tests_table.loc[df_medory_blood_biochemical_tests_table['Year'].isin(choose_year)]
                    
                    st.dataframe(df_medory_blood_biochemical_tests_table.loc[:, ~df_medory_blood_biochemical_tests_table.columns.isin(['Year', 'ID', 'Αφορά Χρήστη'])].T, height = 600, use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

    with col3:
        # For hemtological tests:
        if check3:
            # Get data from medory_hematological_tests:
            def select_all_medory_hematological_tests_table():
                query=con.table("medory_hematological_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_medory_hematological_tests_table()

            # Create dataframe with this data:
            df_medory_hematological_tests_table = pd.DataFrame(query.data)
            
            # Set the columns names:
            if len(df_medory_hematological_tests_table) > 0:
                df_medory_hematological_tests_table.columns = ['ID', 'Created At', _('Ταχύτητα καθίζησης ερυθρών'), _('Βιταμίνη Β 12'), _('Αφορά Χρήστη')]

            # Initialize the container width session:
            #st.checkbox("Use container width", value=True, key="use_container_width3")
            
            # Display the dataframe:
            st.subheader(_("Αιματολογικές Εξετάσεις"))
            st.dataframe(df_medory_hematological_tests_table.T, use_container_width=True)

    with col1:
        # For the level of drugs tests:
        if check4:
            # Get data from medory_drug_levels_tests_table:
            def select_all_from_medory_drug_levels_tests_table():
                query=con.table("medory_drug_levels_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_drug_levels_tests_table()

            # Create dataframe with this data:
            df_medory_drug_levels_tests_table = pd.DataFrame(query.data)
            
            # Set the columns names:
            if len(df_medory_drug_levels_tests_table) > 0:
                df_medory_drug_levels_tests_table.columns = ['ID', 'Created At', _('Τροπονίνη Ι (cTnI)'), _('Αφορά Χρήστη')]

            # Initialize the container width session:
            #st.checkbox("Use container width", value=True, key="use_container_width4")
            
            # Display the dataframe:
            st.subheader(_("Επίπεδα Φαρμάκων"))
            st.dataframe(df_medory_drug_levels_tests_table.T, use_container_width=True)

    with col2:
        # For thyroid tests:
        if check5:
            # Get data from medory_thyroid_check_tests_table:
            def select_all_from_medory_thyroid_check_tests_table():
                query=con.table("medory_thyroid_check_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_thyroid_check_tests_table()

            # Create dataframe with this data:
            df_medory_thyroid_check_tests_table = pd.DataFrame(query.data)
            
            # Set the columns names:
            if len(df_medory_thyroid_check_tests_table) > 0:
                df_medory_thyroid_check_tests_table.columns = ['ID', 'Created At', _('Θυρεοτρόπος ορμονη TSH'), _('Αφορά Χρήστη')]

            # Display the dataframe:
            st.subheader(_("Έλεγχος Θυρεοειδούς"))
            st.dataframe(df_medory_thyroid_check_tests_table.T, use_container_width=True)
        
    with col3:
        
        if check6:
            # Get data from medory_hematological_tests:
            def select_all_from_medory_hematological_tests():
                query=con.table("medory_hematological_tests").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
                return query
            query = select_all_from_medory_hematological_tests()

            # Create dataframe with this data:
            df_medory_hematological_tests = pd.DataFrame(query.data)
            
            # Set the columns names:
            if len(df_medory_hematological_tests) > 0:
                df_medory_hematological_tests.columns = ['ID', 'Created At', 'Σάκχαρο', 'Ουρία', 'Κρεατινίνη', 'Ουρικό οξύ', 'Χοληστερόλη ολική', 
                                    'Τριγλυκερίδια', 'Οξαλοξεική τρανσαμινάση (SGOT)', 'Πυροσταφυλική τρανσαμινάση (SGPT)', 'y-Γλουταμινική τρασφεράση', 'Νάτριο', 
                                    'Κάλιο', 'Ασβέστιο ολικό', 'Σίδηρος', 'Φερριτίνη', 'Αφορά Χρήστη']

            # Initialize the container width session:
            #st.checkbox("Use container width", value=True, key="use_container_width6")
            
            # Display the dataframe:
            st.subheader("Αιματολογικές Εξετάσεις")
            st.dataframe(df_medory_hematological_tests.T, use_container_width=True)




