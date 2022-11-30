import pandas as pd 
import numpy as np
import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import datetime
import gettext
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


st.write("**Αναζήτηση και προβολή αποτελεσμάτων**")

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
        col1, col2, col3 = st.columns(3, gap='large')
        with col1: 
            select_specific_indicator = st.selectbox(_('Θεση A'), options = df_merged.columns )
            df_merged_A = df_merged.dropna(subset=[select_specific_indicator])
            # Drop rows with <NA> values:
            

            if select_specific_indicator != '-':
                choose_date_A = st.multiselect(label = _('Διάλεξε Ημερομηνίες για θέση Α'), options = df_merged_A.index)
                if choose_date_A:
                    # Display the dataframe:
                    df_merged_A = df_merged_A.loc[df_merged_A.index.isin(choose_date_A)]
                
                    #Create the chart;
                    fig3 = px.line(data_frame=df_merged_A, x=choose_date_A,  y=select_specific_indicator)
                    fig3.update_layout(
                        margin=dict(l=0, r=0, t=0, b=40),      #, 
                    )
                    st.write("---")
                    st.write("**Αναλυτικές Πληροφορίες για {}**".format(select_specific_indicator))
                    st.write("Εμφανίζονται οι **{}** τελευταίες καταχωρήσεις για εξέταση δείκτη **{}**.".format(len(df_merged_A), select_specific_indicator) )
                    st.write("Μέγιστη τιμή : **{}** & Ημερομηνία : **{}**".format(max(df_merged_A[select_specific_indicator]),df_merged_A[select_specific_indicator].idxmax()) )
                    st.write("Ελάχιστη τιμή : **{}** & Ημερομηνία : **{}**".format(min(df_merged_A[select_specific_indicator]),df_merged_A[select_specific_indicator].idxmin()) )
                    st.write("Μέσος όρος τιμών, για τις επιλεχθέντες φορές : **{}**".format(df_merged_A[select_specific_indicator].mean()))

                    st.write("#")
                  
                    st.write(_("**Τιμές για {}**").format(select_specific_indicator))
                    st.dataframe(df_merged_A[select_specific_indicator], use_container_width=True)  
                    st.write(_("**Γράφημα για {}**").format(select_specific_indicator))
                    st.plotly_chart(fig3, use_container_width=True)
                 
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))
        with col2:

            select_specific_indicator = st.selectbox(_('Θεση B'), options = df_merged.columns )

            # Drop rows with <NA> values:
            df_merged_B = df_merged.dropna(subset=[select_specific_indicator])
            

            if select_specific_indicator != '-':
                choose_date_B = st.multiselect(label = _('Διάλεξε Ημερομηνίες για θέση Β'), options = df_merged_B.index)
                if choose_date_B:
                    # Display the dataframe:
                    df_merged_B = df_merged_B.loc[df_merged_B.index.isin(choose_date_B)]
                
                    #Create the chart;
                    fig3 = px.bar(data_frame=df_merged_B, x=choose_date_B,  y=select_specific_indicator)
                    fig3.update_layout(
                        margin=dict(l=0, r=0, t=0, b=40),
                    )
                    st.write("---")
                    st.write("**Αναλυτικές Πληροφορίες για {}**".format(select_specific_indicator))
                    st.write("Εμφανίζονται οι **{}** τελευταίες καταχωρήσεις για εξέταση δείκτη **{}**.".format(len(df_merged_B), select_specific_indicator) )
                    st.write("Η μεγαλύτερη τιμή για **{}** είναι **{}** και σε ημερομηνία είναι". format(select_specific_indicator, max(df_merged_B[select_specific_indicator])), df_merged_B[select_specific_indicator].idxmax())
                    st.write("#")
                  
                    st.write(_("**Τιμές για {}**").format(select_specific_indicator))
                    st.dataframe(df_merged_B[select_specific_indicator], use_container_width=True)  
                    st.write(_("**Γράφημα για {}**").format(select_specific_indicator))
                    st.plotly_chart(fig3, use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))
        with col3:
            select_specific_indicator = st.selectbox(_('Θεση C'), options = df_merged.columns )

            # Drop rows with <NA> values:
            df_merged_C = df_merged.dropna(subset=[select_specific_indicator])

            if select_specific_indicator != '-':
                choose_date_C = st.multiselect(label = _('Διάλεξε Ημερομηνίες για θέση C'), options = df_merged_C.index)
                if choose_date_C:
                    # Display the dataframe:
                    df_merged_C = df_merged_C.loc[df_merged_C.index.isin(choose_date_C)]
                
                    #Create the chart;
                    fig3 = px.bar(data_frame=df_merged_C, x=choose_date_C,  y=select_specific_indicator)
                    fig3.update_layout(
                        margin=dict(l=0, r=0, t=0, b=40),
                    )
                    st.write("---")
                    st.write("**Αναλυτικές Πληροφορίες για {}**".format(select_specific_indicator))
                    st.write("Εμφανίζονται οι **{}** τελευταίες καταχωρήσεις για εξέταση δείκτη **{}**.".format(len(df_merged_C), select_specific_indicator) )
                    st.write("Η μεγαλύτερη τιμή για **{}** είναι **{}** και σε ημερομηνία είναι". format(select_specific_indicator, max(df_merged_C[select_specific_indicator])), df_merged_C[select_specific_indicator].idxmax())
                    st.write("#")
                  
                    st.write(_("**Τιμές για {}**").format(select_specific_indicator))
                    st.dataframe(df_merged_C[select_specific_indicator], use_container_width=True)  
                    st.write(_("**Γράφημα για {}**").format(select_specific_indicator))
                    st.plotly_chart(fig3, use_container_width=True)
            else:
                st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

        #-----------End of Create Chart depending on selected indicator and dates -------------#


    else: 
        st.write(_("**Δεν υπάρχουν εγγραφές για το άτομο {}**".format(assign_user)))

    # min_time = int(df_merged.index.min())
    #df.index = pd.to_datetime(df.index)

    df_merged.index = pd.to_datetime(df_merged.index)
    st.write(df_merged.index)


    time = st.slider("Ψάξε με χρονικό εύρος", df_merged_A[select_specific_indicator].idxmin(), df_merged_A[select_specific_indicator].idxmax(), (df_merged_A[select_specific_indicator].idxmin(), df_merged_A[select_specific_indicator].idxmax()), step=100)
    selected_area = (df_merged_A.Rows_Count.between(selected_time_range[0], selected_time_range[1]) )
    df_prepared = pd.DataFrame(df_merged[selected_area])
    df_merged_A


# #################################################################
# def select_all_from_medory_user_table():
#     query=con.table("medory_user_table").select("*").execute()
#     return query
# query = select_all_from_medory_user_table()

# df_medory_user_table = pd.DataFrame(query.data)

# df_medory_user_table_unique_values = df_medory_user_table.copy()
# st.title(_("Αποτελέσματα Τιμών Εξετάσεων Αίματος"))


# assign_user = st.selectbox(_("Αναφορά Χρήστη ") , (df_medory_user_table_unique_values['fullname']))
# row_index = df_medory_user_table_unique_values.index[df_medory_user_table_unique_values['fullname']==assign_user].tolist()


# if assign_user != '':
#     st.sidebar.markdown(_("## Έχεις επιλέξει τον παρακάτω χρήστη."))

#     df_medory_user_table_unique_values['bmi'] = df_medory_user_table_unique_values['weight'] / ((df_medory_user_table_unique_values['height'] / 100) ** 2)
#     st.sidebar.write(_("Όνομα:"), df_medory_user_table_unique_values.loc[row_index[0]]['fullname'])
#     st.sidebar.write(_("Ηλικία:"), df_medory_user_table_unique_values.loc[row_index[0]]['age'])
#     st.sidebar.write(_("Βάρος:"), df_medory_user_table_unique_values.loc[row_index[0]]['weight'])
#     st.sidebar.write(_("Ύψος:"), df_medory_user_table_unique_values.loc[row_index[0]]['height'])
#     st.sidebar.write(_("BMI:"), round(df_medory_user_table_unique_values.loc[row_index[0]]['bmi'],3))
#     with st.expander(_("Πατείστε για άνοιγμα/κλείσιμο"), expanded = True):
#         st.subheader(_("Επίλεξε είδος εξέτασης για τον {}").format(assign_user))
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             check1 = st.checkbox(_("Γενική εξέταση αίματος"))
#             check2 = st.checkbox(_("Βιοχημικές"))
#             check3 = st.checkbox(_("Αιματολογικές Εξετάσεις"))
#             check4 = st.checkbox(_("Επίπεδα Φαρμάκων"))
#             check5 = st.checkbox(_("Έλεγχος Θυρεοειδούς"))
#             check6 = st.checkbox(_("Ορολογικές"))
#         with col2:
#             check7 = st.checkbox("other1")
#             check8 = st.checkbox("other2")
#             check9 = st.checkbox("other3")
#             check10 = st.checkbox("other4")
#             check11 = st.checkbox("other5")
#             check12 = st.checkbox("other6")
#         with col3:
#             check13 = st.checkbox("other7")
#             check14 = st.checkbox("other8")
#             check15 = st.checkbox("other9")
#             check16 = st.checkbox("other10")
#             check17 = st.checkbox("other11")
#             check18 = st.checkbox("other12")
        
#         with col4:
#             check19 = st.checkbox("other13")
#             check20 = st.checkbox("other14")
#             check21 = st.checkbox("other15")
#             check22 = st.checkbox("other16")
#             check23 = st.checkbox("other17")
#             check24 = st.checkbox("other18")

#     st.markdown("""---""")

#     col1, col2, col3 = st.columns(3, gap='large')
#     with col1:
#         # For General Blood Tests
#         if check1:
#             # Get data from medory_general_blood_tests_table:
#             def select_all_from_medory_general_blood_tests_table():
#                 query=con.table("medory_general_blood_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
#                 return query
#             query = select_all_from_medory_general_blood_tests_table()
#             # Create dataframe with this data:
#             df_medory_general_blood_tests_table = pd.DataFrame(query.data)
#             if len(df_medory_general_blood_tests_table) > 0:
#                 # Set the columns names:
#                 df_medory_general_blood_tests_table.columns = ['ID', 'Created At', _('RBC Ερυθρά Αιμοσφαίρια'), _('HGB Αιμοσφαιρίνη'), _('HCT Αιματοκρίτης'), _('MCV Μέσος Όγκος Ερυθρών'), _('MCH Μέση περιεκτικότης'), 
#                             _('MCHC Μέση Συγκέντρωση'), _('RDW Εύρος Κατανομής'), _('WBC Λευκά Αιμοσφαίρια'), _('NEU Ουδετερόφιλα %'), _('LYM Λεμφοκύτταρα %'), 
#                             _('EOS Ηωσινόφιλα %'), _('BASO Βασεόφιλα %'), _('NEU Ουδετερόφιλα #'), _('LYM Λεμφοκύτταρα #'), _('MON Μεγάλα μονοπύρηνα #'), _('EOS Ηωσινόφιλα #'), _('BASO Βασεόφιλα #'),
#                             _('PLT Αιμοπετάλια'), _('PCT Αιμοπεταλιοκρίτης'), _('MPV Μέσος όγκος αιμοπεταλίων'), _('PDW Εύρος Κατανομής-PLT'), _('Αφορά Χρήστη')]
#                 # Set the Create At column to be datetime column:
#                 df_medory_general_blood_tests_table['Created At'] = pd.to_datetime(df_medory_general_blood_tests_table['Created At'])
#                 # Edit this column to keep only year, month and day:
#                 df_medory_general_blood_tests_table['Created At'] = df_medory_general_blood_tests_table['Created At'].dt.strftime('%Y-%m-%d')
#                 # Create new Year column and set this as datetime column:
#                 df_medory_general_blood_tests_table['Year'] = pd.to_datetime(df_medory_general_blood_tests_table['Created At'])
#                 # Edit this Year column to keep only data of Year. We need this to select Year below:
#                 df_medory_general_blood_tests_table['Year'] = df_medory_general_blood_tests_table['Year'].dt.strftime('%Y-%m')
#                 df_medory_general_blood_tests_table.sort_values(by='Year', ascending = False, inplace=True)

#                 # Choose year to display results based on it:
#                 choose_year = st.multiselect(label = _('Διαλέξτε Ημερομηνίες'), options = df_medory_general_blood_tests_table['Year']) 
#                 if choose_year:
#                     # Display the dataframe:
#                     st.subheader(_("Γενική εξέταση αίματος για {}").format(assign_user))
#                     # Edit dataframe to keep data depending on above choose year:
#                     df_medory_general_blood_tests_table = df_medory_general_blood_tests_table.loc[df_medory_general_blood_tests_table['Year'].isin(choose_year)]
#                     # Display dataframe all columns, exclude specidic:
                    

#                     st.dataframe(df_medory_general_blood_tests_table.loc[:, ~df_medory_general_blood_tests_table.columns.isin(['Year', 'ID', 'Αφορά Χρήστη'])].T, height = 800, use_container_width=True)
#             else:
#                 st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

#     with col2:
#         # For Biochemical Tests:
#         if check2:
#             # Get data from medory_blood_biochemical_tests_table:
#             def select_all_from_medory_blood_biochemical_tests_table():
#                 query=con.table("medory_blood_biochemical_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
#                 return query
#             query = select_all_from_medory_blood_biochemical_tests_table()

#             # Create dataframe with this data:
#             df_medory_blood_biochemical_tests_table = pd.DataFrame(query.data)
            
#             # Set the columns names:
#             if len(df_medory_blood_biochemical_tests_table) > 0:
#                 df_medory_blood_biochemical_tests_table.columns = ['ID', 'Created At', _('Σάκχαρο'), _('Ουρία'), _('Κρεατινίνη'), _('Ουρικό οξύ'), _('Χοληστερόλη ολική'), 
#                                     _('Τριγλυκερίδια'), _('Οξαλοξεική τρανσαμινάση (SGOT)'), _('Πυροσταφυλική τρανσαμινάση (SGPT)'), _('y-Γλουταμινική τρασφεράση'), _('Νάτριο'), 
#                                     _('Κάλιο'), _('Ασβέστιο ολικό'), _('Σίδηρος'), _('Φερριτίνη'), _('Αφορά Χρήστη')]

#                 df_medory_blood_biochemical_tests_table['Created At'] = pd.to_datetime(df_medory_blood_biochemical_tests_table['Created At'])
#                 df_medory_blood_biochemical_tests_table['Created At'] = df_medory_blood_biochemical_tests_table['Created At'].dt.strftime('%Y-%m-%d')
#                 df_medory_blood_biochemical_tests_table['Year'] = pd.to_datetime(df_medory_blood_biochemical_tests_table['Created At'])
#                 df_medory_blood_biochemical_tests_table['Year'] = df_medory_blood_biochemical_tests_table['Year'].dt.strftime('%Y-%m')
#                 df_medory_blood_biochemical_tests_table.sort_values(by='Year', ascending = False, inplace=True)

#                 choose_year = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_blood_biochemical_tests_table['Year'])
#                 if choose_year:

#                     # Display the dataframe:
#                     st.subheader(_("Βιοχημικές Αίματος"))
#                     df_medory_blood_biochemical_tests_table = df_medory_blood_biochemical_tests_table.loc[df_medory_blood_biochemical_tests_table['Year'].isin(choose_year)]
                    
#                     st.dataframe(df_medory_blood_biochemical_tests_table.loc[:, ~df_medory_blood_biochemical_tests_table.columns.isin(['Year', 'ID', 'Αφορά Χρήστη'])].T, height = 300, use_container_width=True)
#             else:
#                 st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

#     with col3:
#         # For hemtological tests:
#         if check3:
#             # Get data from medory_hematological_tests_table:
#             def select_all_from_medory_hematological_tests_table():
#                 query=con.table("medory_hematological_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
#                 return query
#             query = select_all_from_medory_hematological_tests_table()

#             # Create dataframe with this data:
#             df_medory_hematological_tests_table = pd.DataFrame(query.data)
            
#             # Set the columns names:
#             if len(df_medory_hematological_tests_table) > 0:
#                 df_medory_hematological_tests_table.columns = ['ID', 'Created At', _('Ταχύτητα καθίζησης ερυθρών'), _('Βιταμίνη Β12'), _('Αφορά Χρήστη')]

#                 df_medory_hematological_tests_table['Created At'] = pd.to_datetime(df_medory_hematological_tests_table['Created At'])
#                 df_medory_hematological_tests_table['Created At'] = df_medory_hematological_tests_table['Created At'].dt.strftime('%Y-%m-%d')
#                 df_medory_hematological_tests_table['Year'] = pd.to_datetime(df_medory_hematological_tests_table['Created At'])
#                 df_medory_hematological_tests_table['Year'] = df_medory_hematological_tests_table['Year'].dt.strftime('%Y-%m')
#                 df_medory_hematological_tests_table.sort_values(by='Year', ascending = False, inplace=True)

#                 choose_year = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_hematological_tests_table['Year'])
#                 if choose_year:

#                     # Display the dataframe:
#                     st.subheader(_("Βιοχημικές Αίματος"))
#                     df_medory_hematological_tests_table = df_medory_hematological_tests_table.loc[df_medory_hematological_tests_table['Year'].isin(choose_year)]
                    
#                     st.dataframe(df_medory_hematological_tests_table.loc[:, ~df_medory_hematological_tests_table.columns.isin(['Year', 'ID', 'Αφορά Χρήστη'])].T, height = 300, use_container_width=True)
#             else:
#                 st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

#     with col1:
#         # For the level of drugs tests:
#         if check4:
#             # Get data from medory_drug_levels_tests_table:
#             def select_all_from_medory_drug_levels_tests_table():
#                 query=con.table("medory_drug_levels_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
#                 return query
#             query = select_all_from_medory_drug_levels_tests_table()

#             # Create dataframe with this data:
#             df_medory_drug_levels_tests_table = pd.DataFrame(query.data)
            
#             # Set the columns names:
#             if len(df_medory_drug_levels_tests_table) > 0:
#                 df_medory_drug_levels_tests_table.columns = ['ID', 'Created At', _('Τροπονίνη - Ι'), _('Αφορά Χρήστη')]

#                 df_medory_drug_levels_tests_table['Created At'] = pd.to_datetime(df_medory_hematological_tests_table['Created At'])
#                 df_medory_drug_levels_tests_table['Created At'] = df_medory_drug_levels_tests_table['Created At'].dt.strftime('%Y-%m-%d')
#                 df_medory_drug_levels_tests_table['Year'] = pd.to_datetime(df_medory_drug_levels_tests_table['Created At'])
#                 df_medory_drug_levels_tests_table['Year'] = df_medory_drug_levels_tests_table['Year'].dt.strftime('%Y-%m')
#                 df_medory_drug_levels_tests_table.sort_values(by='Year', ascending = False, inplace=True)

#                 choose_year = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_hematological_tests_table['Year'])
#                 if choose_year:

#                     # Display the dataframe:
#                     st.subheader(_("Βιοχημικές Αίματος"))
#                     df_medory_drug_levels_tests_table = df_medory_drug_levels_tests_table.loc[df_medory_hematological_tests_table['Year'].isin(choose_year)]
                    
#                     st.dataframe(df_medory_drug_levels_tests_table.loc[:, ~df_medory_drug_levels_tests_table.columns.isin(['Year', 'ID', 'Αφορά Χρήστη'])].T, height = 300, use_container_width=True)
#             else:
#                 st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))

#     with col2:
#         # For thyroid tests:
#         if check5:
#             # Get data from medory_thyroid_check_tests_table:
#             def select_all_from_medory_thyroid_check_tests_table():
#                 query=con.table("medory_thyroid_check_tests_table").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
#                 return query
#             query = select_all_from_medory_thyroid_check_tests_table()

#             # Create dataframe with this data:
#             df_medory_thyroid_check_tests_table = pd.DataFrame(query.data)
            
#             # Set the columns names:
#             if len(df_medory_thyroid_check_tests_table) > 0:
#                 df_medory_thyroid_check_tests_table = ['ID', 'Created At', _('Θυρεοτρόπος ορμόνη (TSH)'), _('Αφορά Χρήστη')]

#                 df_medory_thyroid_check_tests_table['Created At'] = pd.to_datetime(df_medory_hematological_tests_table['Created At'])
#                 df_medory_thyroid_check_tests_table['Created At'] = df_medory_thyroid_check_tests_table['Created At'].dt.strftime('%Y-%m-%d')
#                 df_medory_thyroid_check_tests_table['Year'] = pd.to_datetime(df_medory_thyroid_check_tests_table['Created At'])
#                 df_medory_thyroid_check_tests_table['Year'] = df_medory_thyroid_check_tests_table['Year'].dt.strftime('%Y-%m')
#                 df_medory_thyroid_check_tests_table.sort_values(by='Year', ascending = False, inplace=True)

#                 choose_year = st.multiselect(label = _('Διάλεξε Ημερομηνίες'), options = df_medory_hematological_tests_table['Year'])
#                 if choose_year:

#                     # Display the dataframe:
#                     st.subheader(_("Βιοχημικές Αίματος"))
#                     df_medory_thyroid_check_tests_table = df_medory_thyroid_check_tests_table.loc[df_medory_thyroid_check_tests_table['Year'].isin(choose_year)]
                    
#                     st.dataframe(df_medory_thyroid_check_tests_table.loc[:, ~df_medory_thyroid_check_tests_table.columns.isin(['Year', 'ID', 'Αφορά Χρήστη'])].T, height = 300, use_container_width=True)
#             else:
#                 st.write(_("Δεν υπάρχουν εγγραφές για αυτά τα κριτήρια"))
        
#     with col3:
        
#         if check6:
#             # Get data from medory_hematological_tests:
#             def select_all_from_medory_hematological_tests():
#                 query=con.table("medory_hematological_tests").select("*").eq("user_id", int(df_medory_user_table_unique_values.loc[row_index[0]]['id'])).execute()
#                 return query
#             query = select_all_from_medory_hematological_tests()

#             # Create dataframe with this data:
#             df_medory_hematological_tests = pd.DataFrame(query.data)
            
#             # Set the columns names:
#             if len(df_medory_hematological_tests) > 0:
#                 df_medory_hematological_tests.columns = ['ID', 'Created At', 'Σάκχαρο', 'Ουρία', 'Κρεατινίνη', 'Ουρικό οξύ', 'Χοληστερόλη ολική', 
#                                     'Τριγλυκερίδια', 'Οξαλοξεική τρανσαμινάση (SGOT)', 'Πυροσταφυλική τρανσαμινάση (SGPT)', 'y-Γλουταμινική τρασφεράση', 'Νάτριο', 
#                                     'Κάλιο', 'Ασβέστιο ολικό', 'Σίδηρος', 'Φερριτίνη', 'Αφορά Χρήστη']

#             # Initialize the container width session:
#             #st.checkbox("Use container width", value=True, key="use_container_width6")
            
#             # Display the dataframe:
#             st.subheader("Αιματολογικές Εξετάσεις")
#             st.dataframe(df_medory_hematological_tests.T, use_container_width=True)




