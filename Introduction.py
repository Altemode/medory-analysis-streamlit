import pandas as pd 
import streamlit as st
import gettext
_ = gettext.gettext
from os import system, path
import requests
import pandas as pd


# Set config page
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

# Buttons to generate automitacally commands for the translation:
POT = st.sidebar.button(('POT generate'))
MO = st.sidebar.button('MO generate')
if POT:
    system(f'cd {path.dirname(path.realpath(__file__))} & /usr/lib/python3.10/Tools/i18n/pygettext.py -d base -o locales/base.pot Introduction.py pages/2_Insert_User.py pages/3_Insert_Medical_Data.py')
    system(f'cd {path.dirname(path.realpath(__file__))} && cp locales/base.pot locales/eng/LC_MESSAGES/base.po')

if MO:
    system(f'cd {path.dirname(path.realpath(__file__))} && msgfmt -o locales/eng/LC_MESSAGES/base.mo locales/eng/LC_MESSAGES/base')


# some introduction...
st.title(_("Αρχική σελίδα - Σύντομη περιγραφή!"))

st.write(_("Η εφαρμογή αποτελειται από λειτουργίες οι οποίες εκτελούνται από τις σελίδες που υπάρχουν στο αριστερα κάθετο μενού."))

st.write(_("**Insert User:** Ο χρήστης είναι σε θέση να προσθέσει νέο άτομο με τα στοιχεία του στην βάση δεδομένων."))

st.write(_('**Insert Medical Data:** Ο χρήστης μπορεί να προσθέσει νέα αποτελέσματα εξετάσεων. Αφού επιλέξει για ποιο άτομο αφορούν, κατόπιν επιλέγει το είδος εξέτασης και συμπληρώνει τις τιμές στα ανάλογα πεδία.'))

st.write(_('**Delete Medical Data:** Αυτή η λειτουργία είναι υπό κατασκευή.'))

st.write(_('**Display Medical Data:** Ο χρήστης μπορεί να προβάλει αποτελέσματα εξετάσεων. Αφού επιλεξει για ποιο άτομο ενδιαφέρεται, έπειτα επιλέγει το είδος της εξέτασης και τις χρονολογίες που τον ενδιαφέρουν.'))

st.write(_('**Charts:** Ο χρήστης μπορεί να προβάλει αποτελέσματα εξετάσεων σε γραφήματα. Πρώτα επιλέγει το άτομο που τον ενδιαφέρει, έπειτα το είδος της εξέτασης και τον δείκτη  για να προβαλει σε γράφημα.'))




st.write("H")

response1 = requests.get("https://sportsmetrics.geth.gr")
st.write("sportsmetrics",response1)

response2 = requests.get("https://geth.gr")
st.write("geth",response2)

response3 = requests.get("https://paramithenios.gr")
st.write("plottwist",response3)

response3 = requests.get("https://artdigital.gr")
st.write("art",response3)



dftest1 = pd.read_csv("https://paramithenios.gr/testfolder/testOther.csv")
st.write("parami testOther", dftest1)

dftest2 = pd.read_csv("https://sportsmetrics.geth.gr/storage/TestBeta.csv")
st.write("dftest 1", dftest2)
