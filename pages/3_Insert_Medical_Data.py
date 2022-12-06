import pandas as pd 
import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import numpy as np
import random
from random import randrange
from datetime import timedelta
from datetime import datetime
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

# Fetch all users from user_table:
def select_all_from_medory_user_table():
    query=con.table("medory_user_table").select("*").execute()
    return query
query = select_all_from_medory_user_table()
df_medory_user_table = pd.DataFrame(query.data)
df_medory_user_table_unique_values = df_medory_user_table.copy()

#---- Insert random sample data -----#
insert_demo_data = st.sidebar.button(_('Εισαγωγή τυχαίων δεδομένων, για Γενική Αίματος'))
if insert_demo_data:
    # Create def for random date at created_at column:
    def random_date(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)
    d1 = datetime.strptime('1/1/2016 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('11/11/2022 4:50 AM', '%m/%d/%Y %I:%M %p')
    # Define random range data:
    number_list = random.sample(range(1, 50), 7)
    # Define the ids of the users:
    user_id_list = [6,7,8]
    # Def to insert random sample data: 
    def add_entries_to_medory_general_blood_tests_table(supabase):
        value = {'created_at':str(random_date(d1, d2)), 'rbc': random.choice(number_list), 'hgb': random.choice(number_list), 'hct': random.choice(number_list), 'mcv': random.choice(number_list), 'mch': random.choice(number_list), 'rdw': random.choice(number_list),
                'wbc': random.choice(number_list), 'neu1': random.choice(number_list), 'lym1': random.choice(number_list), 'mon1': random.choice(number_list), 'eos1': random.choice(number_list), 'baso1': random.choice(number_list),
                'neu2': random.choice(number_list), 'lym2': random.choice(number_list), 'mon2': random.choice(number_list), 'eos2': random.choice(number_list), 'baso2': random.choice(number_list),
                'plt': random.choice(number_list), 'pct': random.choice(number_list), 'mpv': random.choice(number_list), 'pdw': random.choice(number_list), 'user_id': random.choice(user_id_list)}
        data = supabase.table('medory_general_blood_tests_table').insert(value).execute()
    def main():
        new_entry = add_entries_to_medory_general_blood_tests_table(con)
    main()
    st.sidebar.success(_('Μία νέα εισαγωγή με τυχαίες τιμές έχει εισαχθεί στην βάση δεδομένων.', icon="✅"))
#---- End of Insert random sample data -----#


st.title(_("Εισαγωγή Τιμών Εξετάσεων"))
assign_user = st.selectbox(_("Αναφορά Χρήστη") , (df_medory_user_table_unique_values['fullname']))
row_index = df_medory_user_table_unique_values.index[df_medory_user_table_unique_values['fullname']==assign_user].tolist()
st.write("#")
st.caption(_("Επίλεξε κατηγορία εξέτασης"))
tab1, tab2, tab3, tab4 = st.tabs(["Εξέταση Αίματος", "Μαγνητικές", "Ακτινογραφίες","Υπέρηχοι"])
with tab1:
    st.write("#")
    st.markdown(_("Κατευθυνθείτε στο οριζόντιο μενού ώστε να εισαγάγετε νέες τιμές εξετάσεων."))
    # 2. horizontal menu
    selected = option_menu(None, [_("Γενική αίματος"), _("Βιοχημικές"), _("Αιματολογικές"), _('Επίπεδα Φαρμάκων'), _('Έλεγχος Θυρεοειδούς'), _('Ορολογικές'), _('Βιταμίνες')], 
        icons=['house', 'cloud-upload', "list-task", 'gear'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {'font-size':'12px !important', 'font-weight': '900', 'width': '2100 !important', "padding": "0 !important", "margin": "0 !important", "background-color": "#fafafa"},
            "icon": { "font-size": "15px"}, 
            "nav-link": { "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            #"nav-link-selected": {"background-color": "green"},
        })



    

    ###### ######### ########## INSERT DATA for medory_general_blood_tests_table ########## ########## ##########
    if selected == _('Γενική αίματος'):

        # Insert real data for medory_general_blood_tests_table
        st.write(_("**Γενική αίματος**"))
        # Columns with fields to insert values:
        with st.form(_("Εισαγωγή τιμών εξέτασης αίματος"), clear_on_submit=False):
            with st.expander(_("Ερυθρά Σειρά")):
                col1,col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1],  gap="medium") 
                with col1: RBC = st.number_input(_("RBC Ερυθρά Αιμοσφαίρια"))
                with col2: HGB = st.number_input(_("HGB Αιμοσφαιρίνη"))
                with col3: HCT = st.number_input(_("HCT Αιματοκρίτης"))
                with col4: MCV = st.number_input(_("MCV Μέσος Όγκος Ερυθρών"))
                with col5: MCH = st.number_input(_("MCH Μέση περιεκτικότης"))
                with col6: MCHC = st.number_input(_("MCHC Μέση Συγκέντρωση"))
                with col1: RDW = st.number_input(_("RDW Εύρος Κατανομής"))

            with st.expander(_("Λευκά Σειρά")):
                col1,col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1],  gap="medium") 
                with col1: WBC = st.number_input(_("WBC Λευκά Αιμοσφαίρια"))
                with col2: NEU1 = st.number_input(_("NEU Ουδετερόφιλα %"))
                with col3: LYM1 = st.number_input(_("LYM Λεμφοκύτταρα %"))
                with col4: MON1 = st.number_input(_("MON Μεγάλα Μονοπύρηνα %"))
                with col5: EOS1 = st.number_input(_("EOS Ηωσινόφιλα %"))
                with col6: BASO1 = st.number_input(_("BASO Βασεόφιλα %"))

                with col1: NEU2 = st.number_input(_("NEU Ουδετερόφιλα #"))
                with col2: LYM2 = st.number_input(_("LYM Λεμφοκύτταρα #"))
                with col3: MON2 = st.number_input(_("MON Μεγάλα μονοπύρηνα #"))
                with col4: EOS2 = st.number_input(_("EOS Ηωσινόφιλα #"))
                with col5: BASO2 = st.number_input(_("BASO Βασεόφιλα #"))

                with col6: PLT = st.number_input(_("PLT Αιμοπετάλια"))
                with col1: PCT = st.number_input(_("PCT Αιμοπεταλιοκρίτης"))
                with col2: MPV = st.number_input(_("MPV Μέσος όγκος αιμοπεταλίων"))
                with col3: PDW = st.number_input(_("PDW Εύρος Κατανομής-PLT"))

            submitted = st.form_submit_button(_("Εισαγωγή Τιμών"))

            # If submitted button and assing user insert those values to database:
            if submitted:
                if assign_user != '':
                    def add_entries_to_medory_general_blood_tests_table(supabase):
                            value = {'rbc': RBC, 'hgb': HGB, 'hct': HCT, 'mcv': MCV, 'mch': MCH, 'rdw': RDW,
                                    'wbc': WBC, 'neu1': NEU1, 'lym1': LYM1, 'mon1': MON1, 'eos1': EOS1, 'baso1': BASO1,
                                    'neu2': NEU2, 'lym2': LYM2, 'mon2': MON2, 'eos2': EOS2, 'baso2': BASO2,
                                    'plt': PLT, 'pct': PCT, 'mpv': MPV, 'pdw': PDW, 'user_id': int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])}
                            data = supabase.table('medory_general_blood_tests_table').insert(value).execute()
                    def main():
                        new_entry = add_entries_to_medory_general_blood_tests_table(con)
                    main()
                    st.success(_('Μία καινούρια εγγραφή ιατρικών δεδομένων έχει εισαχθεί στην βάση δεδομένων.'))

                else:
                    st.warning(_("Παρακαλώ επιλέξτε χρήστη!"))

    ###### ######### ########## INSERT DATA for medory_blood_biochemical_tests_table ########## ########## ##########

    if selected == _('Βιοχημικές'):

        # Insert data for medory_general_blood_tests_table
        st.write(_("**Βιοχημικές**"))

        with st.form(_("Εισαγωγή τιμών"), clear_on_submit=False):
            with st.expander(_("Τιμές Βιοχημικών Εξετάσεων")):
                col1,col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1],  gap="medium") 
                with col1: GLU = st.number_input(_("Σάκχαρο"))
                with col2: URE = st.number_input(_("Ουρία"))
                with col3: CRE = st.number_input(_("Κρεατινίνη"))
                with col4: URCA = st.number_input(_("Ουρικό οξύ"))
                with col5: HDL = st.number_input(_("Χοληστερόλη ολική"))
                with col1: TRI = st.number_input(_("Τριγλυκερίδια"))
                with col2: SGOT = st.number_input(_("Οξαλοξεική τρανσαμινάση (SGOT)"))
                with col3: SGPT = st.number_input(_("Πυροσταφυλική τρανσαμινάση (SGPT)"))
                with col4: YGT = st.number_input(_("y-Γλουταμινική τρασφεράση"))
                with col5: NA = st.number_input(_("Νάτριο"))
                with col1: K = st.number_input(_("Κάλιο"))
                with col2: CA = st.number_input(_("Ασβέστιο ολικό"))
                with col3: FE = st.number_input(_("Σίδηρος"))
                with col4: FER = st.number_input(_("Φερριτίνη"))
            

            submitted = st.form_submit_button(_("Εισαγωγή Τιμών"))

            if submitted:
                if assign_user != '':
                    def add_entries_to_medory_blood_biochemical_tests_table(supabase):
                            value = {'glu': GLU, 'ure': URE, 'cre': CRE, 'urca': URCA, 'hdl': HDL, 'tri': TRI,
                                    'sgot': SGOT, 'sgpt': SGPT, 'ygt': YGT, 'na': NA, 'k': K, 'ca': CA,
                                    'fe': FE, 'fer': FER, 'user_id': int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])}
                            data = supabase.table('medory_blood_biochemical_tests_table').insert(value).execute()
                    def main():
                        new_entry = add_entries_to_medory_blood_biochemical_tests_table(con)
                    main()
                    st.success(_('Μία καινούρια εγγραφή ιατρικών δεδομένων έχει εισαχθεί στην βάση δεδομένων.'))
                else:
                    st.warning(_("Παρακαλώ επιλέξτε χρήστη!"))
                    


    ###### ######### ########## INSERT DATA for medory_blood_biochemical_tests_table ########## ########## ##########

    if selected == _('Αιματολογικές'):
        # Insert data for medory_general_blood_tests_table
        st.write(_("**Αιματολογικές**"))

        with st.form(_("Εισαγωγή τιμών"), clear_on_submit=False):
            with st.expander(_("Τιμές Αιματολογικών Εξετάσεων")):
                col1,col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1],  gap="medium") 
                with col1: TKE = st.number_input(_("Ταχύτητα καθίζησης ερυθρών"))
                with col2: B12 = st.number_input(_("Βιταμίνη Β 12"))
                
            submitted = st.form_submit_button(_("Εισαγωγή Τιμών"))

            if submitted:
                if assign_user != '':
                    def add_entries_to_medory_hematological_tests_table(supabase):
                            value = {'tke': TKE, 'b12': B12}
                            data = supabase.table('medory_hematological_tests_table').insert(value).execute()
                    def main():
                        new_entry = add_entries_to_medory_hematological_tests_table(con)
                    main()
                    st.success(_('Μία καινούρια εγγραφή ιατρικών δεδομένων έχει εισαχθεί στην βάση δεδομένων.'))
                else:
                    st.warning(_("Παρακαλώ επιλέξτε χρήστη!"))


    ###### ######### ########## INSERT DATA for medory_drug_levels_tests_table ########## ########## ##########

    if selected == _('Επίπεδα Φαρμάκων'):
        # Insert data for medory_drug_levels_tests_table
        st.write(_("**Επίπεδα Φαρμάκων**"))

        with st.form(_("Εισαγωγή τιμών"), clear_on_submit=False):
            with st.expander(_("Τιμές για Επίπεδα Φαρμάκων")):
                col1,col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1],  gap="medium") 
                with col1: CTNI = st.number_input(_("Τροπονίνη Ι (cTnI)"))
                
            submitted = st.form_submit_button(_("Εισαγωγή Τιμών"))

            if submitted:
                if assign_user != '':
                    def add_entries_to_medory_drug_levels_tests_table(supabase):
                            value = {'ctni': CTNI}
                            data = supabase.table('medory_drug_levels_tests_table').insert(value).execute()
                    def main():
                        new_entry = add_entries_to_medory_drug_levels_tests_table(con)
                    main()
                    st.success(_('Μία καινούρια εγγραφή ιατρικών δεδομένων έχει εισαχθεί στην βάση δεδομένων.'))
                else:
                    st.warning(_("Παρακαλώ επιλέξτε χρήστη!"))

        
    ###### ######### ########## INSERT DATA for medory_thyroid_check_tests_table ########## ########## ##########

    if selected == _('Έλεγχος Θυρεοειδούς'):
        # Insert data for medory_thyroid_check_tests_table
        st.subheader(_("Έλεγχος Θυρεοειδούς"))

        with st.form(_("Εισαγωγή τιμών"), clear_on_submit=False):
            with st.expander(_("Τιμές για έλεγχο Θυρεοειδούς")):
                col1,col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1],  gap="medium") 
                with col1: TSH = st.number_input(_("Θυρεοτρόπος ορμονη TSH"))
                
            submitted = st.form_submit_button(_("Εισαγωγή Τιμών"))

            if submitted:
                if assign_user != '':
                    def add_entries_to_medory_thyroid_check_tests_table(supabase):
                            value = {'tsh': TSH}
                            data = supabase.table('medory_thyroid_check_tests_table').insert(value).execute()
                    def main():
                        new_entry = add_entries_to_medory_thyroid_check_tests_table(con)
                    main()
                    st.success(_('Μία καινούρια εγγραφή ιατρικών δεδομένων έχει εισαχθεί στην βάση δεδομένων.'))
                else:
                    st.warning(_("Παρακαλώ επιλέξτε χρήστη!"))

                
    ###### ######### ########## INSERT DATA for medory_serological_tests_table ########## ########## ##########

    if selected == _('Ορολογικές'):
        # Insert data for medory_serological_tests_table
        st.subheader(_("Ορολογικές"))

        with st.form(_("Εισαγωγή τιμών"), clear_on_submit=False):
            with st.expander(_("Τιμές για Ορολογικές")):
                col1,col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1],  gap="medium") 
                with col1: CRP = st.number_input(_("C-αντιδρώσα (ποσοτική) πρωτείνη (CRP)"))
                
            submitted = st.form_submit_button(_("Εισαγωγή Τιμών"))

            if submitted:
                if assign_user != '':
                    def add_entries_to_medory_serological_tests_table(supabase):
                            value = {'crp': CRP}
                            data = supabase.table('medory_serological_tests_table').insert(value).execute()
                    def main():
                        new_entry = add_entries_to_medory_serological_tests_table(con)
                    main()
                    st.success(_('Μία καινούρια εγγραφή ιατρικών δεδομένων έχει εισαχθεί στην βάση δεδομένων.'))
                else:
                    st.warning(_("Παρακαλώ επιλέξτε χρήστη!"))


    ###### ######### ########## INSERT DATA for medory_vitamins_tests_table ########## ########## ##########


    if selected == _('Βιταμίνες'):
        # Insert data for medory_vitamins_tests_table
        st.subheader(_("Βιταμίνες"))

        with st.form(_("Εισαγωγή τιμών"), clear_on_submit=False):
            with st.expander(_("Τιμές για Βιταμίνες")):
                col1,col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1],  gap="medium") 
                with col1: D3 = st.number_input(_("Βιταμίνη 25OH D3"))
                
            submitted = st.form_submit_button(_("Εισαγωγή Τιμών"))

            if submitted:
                if assign_user != '':
                    def add_entries_to_medory_vitamins_tests_table(supabase):
                            value = {'25OH_D3': D3}
                            data = supabase.table('medory_vitamins_tests_table').insert(value).execute()
                    def main():
                        new_entry = add_entries_to_medory_vitamins_tests_table(con)
                    main()
                    st.success(_('Μία καινούρια εγγραφή ιατρικών δεδομένων έχει εισαχθεί στην βάση δεδομένων.'))
                else:
                    st.warning(_("Παρακαλώ επιλέξτε χρήστη!"))

with tab2:
    st.write("")
    with st.form(_("Εισήγαγε μαγνητική εξέταση"), clear_on_submit=False):
        col1,col2 = st.columns([1, 1,],  gap="medium") 
        with col1:
            diagnosis = st.text_area(_("Διάγνωση"))
        with col2:
            image_1 = st.file_uploader("1η Φωτογραφία")
            image_2 = st.file_uploader("2η Φωτογραφία")
            video = st.file_uploader("Video")            
        submitted = st.form_submit_button(_("Εισαγωγή Εξέτασης"))

        if submitted:
            if assign_user != '':
                def add_entries_to_medory_magnetic_tests_table(supabase):
                        value = {'diagnosis': diagnosis}
                        data = supabase.table('medory_magnetic_tests_table').insert(value).execute()
                def main():
                    new_entry = add_entries_to_medory_magnetic_tests_table(con)
                main()
                st.success(_('Μία καινούρια εγγραφή ιατρικών δεδομένων έχει εισαχθεί στην βάση δεδομένων.'))
            else:
                st.warning(_("Παρακαλώ επιλέξτε χρήστη!"))
        


with tab3:
    st.write("dasda")
    tab11, tab21 = st.tabs(["Εξέταση Αίματος", "Μαγνητικές"])
    with tab11:
        st.write("Ypotabe")


