import pandas as pd 
import streamlit as st
from supabase import create_client, Client

st.set_page_config(
    page_title="Tefaa Metrics",
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

st.title("Εισαγωγή νέου χρήστη")
st.markdown("Παρακαλώ όπως συμπληρώσετε τα παρακάτω πεδία για την εισαγωγή νέου χρήστη στην βάση δεδομένων.")
# Create the form to insert new user in database:
with st.form("Type the ID of your link:", clear_on_submit=False):   
    col1, col2, col3, col4, col5, = st.columns([1, 1, 1, 1, 1],  gap="small") 
    fullname = col1.text_input("Όνομα")
    age = col2.number_input("Ηλικία", value = 0, min_value=0, max_value=100, step=1)
    weight = col3.number_input("Βάρος")
    height = col4.number_input("Ύψος", value = 0, min_value=0, max_value=230, step=1)
    submitted = st.form_submit_button("Εισαγωγή")

    if submitted:
        if fullname and age and weight and height !='-' :
            # Insert new entry in the database users table:
            def add_entries_to_medory_user_table(supabase):
                value = {'fullname': fullname, "age": age, "weight": weight, "height": height}
                data = supabase.table('medory_user_table').insert(value).execute()
            def main():
                new_entry = add_entries_to_medory_user_table(con)
            main()
            st.success(_('Ένας νέος χρήστης έχει εισαχθεί στην βάση δεδομένων.'))
            st.write(list)
        else:
            st.error(_("Κάποιο από τα πεδία δεν έχει συμπληρωθεί."))
# Select ALl Users:
def select_all_from_medory_user_table():
    query=con.table("medory_user_table").select("*").execute()
    return query

query = select_all_from_medory_user_table()
# Create dataframe with the users:
df_all_medory_user_table = pd.DataFrame(query.data)

# Copy dataframe
df = df_all_medory_user_table.copy()

# Find the BMI dataframe column:
df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)

# Set the columns names:
df.columns = ['ID', 'Created At', 'Fullname', 'Age', 'Weight', 'Height', 'BMI']

# # Initialize the container width session:
# st.checkbox("Use container width", value=True, key="use_container_width")

# # Display dataframe with users:
# st.dataframe(df, use_container_width=st.session_state.use_container_width)




