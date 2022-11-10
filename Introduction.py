import pandas as pd 
import streamlit as st
import gettext
_ = gettext.gettext

from os import system, path

import pandas as pd
import numpy as np
import altair as alt

language = st.sidebar.selectbox('', ['eng', 'gr'])
try:
  localizator = gettext.translation('base', localedir='locales', languages=[language])
  localizator.install()
  _ = localizator.gettext 
except:
    pass



POT = st.sidebar.button(('POT generate'))
MO = st.sidebar.button('MO generate')
if POT:
    system(f'cd {path.dirname(path.realpath(__file__))} & /usr/lib/python3.10/Tools/i18n/pygettext.py -d base -o locales/base.pot Introduction.py pages/2_Insert_User.py pages/3_Insert_Medical_Data.py')
    system(f'cd {path.dirname(path.realpath(__file__))} && cp locales/base.pot locales/eng/LC_MESSAGES/base.po')

if MO:
    system(f'cd {path.dirname(path.realpath(__file__))} && msgfmt -o locales/eng/LC_MESSAGES/base.mo locales/eng/LC_MESSAGES/base')


st.title(_("Αρχική σελίδα - περιγραφή εφαρμογής!"))